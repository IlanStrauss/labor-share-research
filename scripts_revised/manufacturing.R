# =====================================================================
# manufacturing.R  —  live US industry shift-share of the labor share
#
# Implements the Gutierrez-Piton (2019) Melitz-Polanec decomposition on
# REAL data from BEA GDP-by-Industry (Components of Value Added, TVA113),
# cached from GDPbyInd.zip (no API key). BEA's industry accounts start in
# 1997, so this covers 1997-2024 (G-P used EU KLEMS for 1977-2015).
#
#   dLS = SUM_k [ wbar_k * dLS_k ]      (within-industry)
#       + SUM_k [ (LSbar_k - LSbar) * dw_k ]  (between-industry)
# =====================================================================
suppressMessages({library(readxl); library(dplyr)})

VA_XLSX <- "data/bea_raw/gdpind/ValueAdded.xlsx"

# Standard non-overlapping BEA summary sectors (private) + Government.
SECTORS <- c(
  "Agriculture, forestry, fishing, and hunting","Mining","Utilities","Construction",
  "Manufacturing","Wholesale trade","Retail trade","Transportation and warehousing",
  "Information","Finance and insurance","Real estate and rental and leasing",
  "Professional and business services",
  "Educational services, health care, and social assistance",
  "Arts, entertainment, recreation, accommodation, and food services",
  "Other services, except government","Government")

# parse TVA113 (Components of Value Added, $M): VA row + its Compensation row
load_industry_va <- function(path = VA_XLSX) {
  raw <- as.data.frame(read_excel(path, "TVA113-A", col_names = FALSE))
  yrs <- suppressWarnings(as.integer(raw[8, ]))
  ycols <- which(!is.na(yrs)); years <- yrs[ycols]
  nm <- trimws(raw[[2]])
  numify <- function(i) suppressWarnings(as.numeric(unlist(raw[i, ycols])))
  get_sector <- function(sec) {
    ix <- which(nm == sec)
    ix <- ix[!is.na(suppressWarnings(as.numeric(raw[ix, ycols[1]])))]   # the VA line
    if (!length(ix)) stop("sector not found: ", sec)
    i <- ix[1]
    stopifnot(trimws(raw[[2]][i+1]) == "Compensation of employees")
    list(va = numify(i), comp = numify(i+1))
  }
  va <- sapply(SECTORS, function(s) get_sector(s)$va)
  comp <- sapply(SECTORS, function(s) get_sector(s)$comp)
  list(years = years,
       va   = as.data.frame(va,   row.names = NULL),
       comp = as.data.frame(comp, row.names = NULL),
       gdp  = numify(which(nm == "Gross domestic product")[1]))
}

# Melitz-Polanec shift-share between two years
shift_share <- function(t0 = 1997, t1 = 2024, dat = load_industry_va()) {
  i0 <- match(t0, dat$years); i1 <- match(t1, dat$years)
  VA0 <- unlist(dat$va[i0, ]);  VA1 <- unlist(dat$va[i1, ])
  C0  <- unlist(dat$comp[i0, ]); C1 <- unlist(dat$comp[i1, ])
  tot0 <- sum(VA0); tot1 <- sum(VA1)
  w0 <- VA0/tot0; w1 <- VA1/tot1
  ls0 <- C0/VA0*100; ls1 <- C1/VA1*100
  LS0 <- sum(C0)/tot0*100; LS1 <- sum(C1)/tot1*100          # aggregate labor share
  wbar <- (w0+w1)/2; lsbar_k <- (ls0+ls1)/2; LSbar <- (LS0+LS1)/2
  within  <- wbar*(ls1-ls0)
  between <- (lsbar_k - LSbar)*(w1-w0)
  res <- data.frame(sector = SECTORS,
                    LS_t0 = ls0, LS_t1 = ls1, dLS = ls1-ls0,
                    w_t1 = w1*100,
                    within_pp = within, between_pp = between,
                    total_pp = within + between,
                    row.names = NULL)
  attr(res, "agg") <- c(t0=t0, t1=t1, LS0=LS0, LS1=LS1, dLS=LS1-LS0,
                        gdp_covered = tot1/dat$gdp[i1])
  res[order(res$total_pp), ]
}
