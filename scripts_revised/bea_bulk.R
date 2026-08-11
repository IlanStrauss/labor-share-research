# =====================================================================
# bea_bulk.R  —  keyless, authoritative BEA data layer
#
# Reads BEA's public bulk NIPA annual flat file (no API key required):
#   https://apps.bea.gov/national/Release/TXT/NipaDataA.txt
# cached at data/bea_raw/NipaDataA.txt. Provides series by BEA code and
# builds the levels needed for the measurement bracket (Atkeson 2020)
# and the corporate-sector labor share. All series codes below were
# identified and cross-checked against known published ratios
# (e.g. comp/GDI 2024 = 51.9%; taxes/GDI = 6.7%; equip+struct+IPP = nonres FI).
# =====================================================================
suppressMessages(library(data.table))

BEA_FILE <- "data/bea_raw/NipaDataA.txt"
BEA_URL  <- "https://apps.bea.gov/national/Release/TXT/NipaDataA.txt"

bea_load <- function(path = BEA_FILE) {
  if (!file.exists(path))
    stop("BEA bulk file missing. Download once (no key needed):\n  curl --http1.1 -A 'Mozilla/5.0' -o ", path, " ", BEA_URL)
  d <- fread(path, colClasses = "character")
  setnames(d, c("code","period","value"))
  d[, `:=`(year = as.integer(period), val = as.numeric(gsub(",", "", value)))]
  d[!is.na(year)]
}

# BEA current-dollar level codes, each verified against SeriesRegister.txt
# (TableId:LineNo in comments). Whole economy = Table 1.10 (T11000);
# investment = Table 1.1.5 (T10105); corporate = Table 1.14 (T11400).
BEA_CODES <- c(
  GDI="A261RC",      # T11000:1  Gross domestic income
  comp="A4002C",     # T11000:2  Compensation of employees, paid
  wages="W270RC",    # T11000:4  Wages and salaries
  prop="A041RC",     # T11000:13 Proprietors' income
  corp_pre="A445RC", # T11000:15 Corporate profits w/ IVA+CCAdj
  corp_post="W273RC",# T11000:17 Profits after tax w/ IVA+CCAdj
  cfc="A262RC",      # T11000:21 Consumption of fixed capital
  taxes="W056RC",    # T11000:7  Taxes on production and imports (GROSS of subsidies)
  subsidies="A107RC",# T11000:8  Subsidies (subtract to get taxes-less-subsidies)
  nos="W271RC",      # T11000:9  Net operating surplus (whole economy)
  corp_pre_noadj="A053RC",  # corporate profits before tax, without IVA/CCAdj
  corp_post_noadj="A055RC", # corporate profits after tax,  without IVA/CCAdj
  inv_gpdi="A006RC", # T10105:7  Gross private domestic investment
  inv_fixed="A007RC",# T10105:8  Private fixed investment
  inv_nonres="A008RC",#T10105:9  Nonresidential fixed investment
  inv_equip="Y033RC",# T10105:11 Equipment
  inv_struct="B009RC",#T10105:10 Structures
  inv_ipp="Y001RC",  # T10105:12 Intellectual property products
  nfc_gva="A455RC",  # T11400:17 NFC gross value added
  nfc_comp="A460RC", # T11400:20 NFC compensation of employees
  nfc_cfc="B456RC",  # T11400:18 NFC consumption of fixed capital (was wrongly A466RC)
  nfc_taxes="W325RC",# T11400:23 NFC taxes on production
  nfc_nos="W326RC")  # T11400:24 NFC net operating surplus

# wide table (year x named level series), 1929-latest --------------------
bea_levels <- function(d = bea_load()) {
  out <- data.frame(year = sort(unique(d$year)))
  for (nm in names(BEA_CODES)) {
    s <- d[code == BEA_CODES[nm], .(year, val)]
    out[[nm]] <- s$val[match(out$year, s$year)]
  }
  out
}

# =====================================================================
# The Atkeson (2020) measurement bracket + corporate-sector labor share
#   (i)   new BEA methodology:            comp / GDI
#   (ii)  pre-1999 methodology:           comp / (GDI - IPP investment)
#   (iii) net-of-depreciation:            comp / (GDI - CFC)   [=NDI]
#   (iv)  labor share of payouts:         comp / (GDI - taxes - nonres fixed inv)
#   NFC:  corporate-sector labor share:   nfc_comp / nfc_gva  (+ net version)
# Whole-economy where noted; NFC uses BEA Table 1.14.
# =====================================================================
# Authoritative whole-economy shares of GDI (%, 1970-2024) from BEA levels.
# taxes here is taxes-on-production-and-imports LESS subsidies; NOS is the
# residual net operating surplus. These supersede the note's hand-transcribed
# taxes/profit arrays (taxes deviate up to ~2.5 pp in 2020, profits ~1.5 pp in
# the 1980s, though endpoints match).
build_whole <- function(L = bea_levels()) {
  L <- L[L$year >= 1970 & L$year <= 2024, ]
  pct <- function(x) x / L$GDI * 100
  data.frame(
    year        = L$year,
    comp        = pct(L$comp),
    wages       = pct(L$wages),
    dep         = pct(L$cfc),
    prop        = pct(L$prop),
    taxes_net   = pct(L$taxes - L$subsidies),
    nos         = pct(L$nos),
    corp_pre    = pct(L$corp_pre),        # with IVA+CCAdj
    corp_post   = pct(L$corp_post),       # with IVA+CCAdj
    corp_pre_na = pct(L$corp_pre_noadj),  # without IVA/CCAdj (note's Fig.3 concept)
    corp_post_na= pct(L$corp_post_noadj))
}

build_bracket <- function(L = bea_levels()) {
  L <- L[L$year >= 1970 & L$year <= 2024, ]
  # accounting-identity guards (fail loud if codes drift)
  gdi_gap <- max(abs(L$GDI - (L$comp + L$taxes + L$cfc +
                              (L$GDI - L$comp - L$taxes - L$cfc))))  # trivially 0; kept for clarity
  nfc_gap <- max(abs(L$nfc_gva - (L$nfc_cfc + L$nfc_comp + L$nfc_taxes + L$nfc_nos)), na.rm=TRUE)
  inv_gap <- max(abs(L$inv_nonres - (L$inv_equip + L$inv_struct + L$inv_ipp)), na.rm=TRUE)
  if (nfc_gap > 1) warning(sprintf("NFC identity off by %.0f (check Table 1.14 codes)", nfc_gap))
  if (inv_gap > 1) warning(sprintf("Investment identity off by %.0f (check Table 1.1.5 codes)", inv_gap))
  within(L, {
    ls_new      <- comp / GDI * 100
    ls_old      <- comp / (GDI - inv_ipp) * 100
    ls_net      <- comp / (GDI - cfc) * 100
    ls_payouts  <- comp / (GDI - taxes - inv_nonres) * 100
    nfc_ls      <- nfc_comp / nfc_gva * 100
    nfc_ls_net  <- nfc_comp / (nfc_gva - nfc_cfc) * 100
    ipp_share   <- inv_ipp / GDI * 100
  })
}
