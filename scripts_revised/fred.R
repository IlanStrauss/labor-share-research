# =====================================================================
# fred.R  —  FRED data layer for the labor-share replication
#
# Strategy: fetch each series LIVE from the FRED JSON API when an API key
# is available (FRED_API_KEY in the environment / ~/.Renviron); otherwise
# fall back to the verified static values transcribed from the original
# Python scripts (which were verified against FRED, Jan 2026). Every
# series reports whether it came from "live" or "static" so the run is
# transparent and reproducible either way.
#
# Get a free key (30s): https://fredaccount.stlouisfed.org/apikeys
# Then add to ~/.Renviron:   FRED_API_KEY=your_key_here
# =====================================================================

suppressMessages({
  library(httr)
  library(jsonlite)
})

# --- Low-level FRED JSON API call (annual observations) --------------
fred_get <- function(series_id, api_key,
                     obs_start = "1970-01-01", obs_end = "2024-12-31") {
  resp <- httr::GET(
    "https://api.stlouisfed.org/fred/series/observations",
    query = list(
      series_id         = series_id,
      api_key           = api_key,
      file_type         = "json",
      observation_start = obs_start,
      observation_end   = obs_end,
      frequency         = "a",          # annual
      aggregation_method = "avg"
    ),
    httr::timeout(30)
  )
  httr::stop_for_status(resp)
  obs <- jsonlite::fromJSON(rawToChar(resp$content))$observations
  data.frame(
    year  = as.integer(substr(obs$date, 1, 4)),
    value = suppressWarnings(as.numeric(obs$value))
  )
}

# --- Fetch-or-fallback wrapper --------------------------------------
# `fallback` is a data.frame(year, value). Returns list(src, data).
get_series <- function(series_id, fallback, api_key, label = series_id, ...) {
  if (is.null(api_key) || !nzchar(api_key)) {
    message(sprintf("  [static] %-22s %s", series_id, label))
    return(list(src = "static", data = fallback))
  }
  out <- tryCatch(fred_get(series_id, api_key, ...), error = function(e) {
    message(sprintf("  [static] %-22s %s  (live fetch failed: %s)",
                    series_id, label, conditionMessage(e)))
    NULL
  })
  if (is.null(out) || nrow(out) == 0 || all(is.na(out$value))) {
    return(list(src = "static", data = fallback))
  }
  message(sprintf("  [ LIVE ] %-22s %s  (%d obs)", series_id, label, nrow(out)))
  list(src = "live", data = out)
}

# =====================================================================
# VERIFIED STATIC FALLBACK VALUES  (share of GDI, %, annual 1970–2024)
# Transcribed from generate_chart.py; verified against FRED Jan 2026.
# =====================================================================
YEARS <- 1970:2024

.fb <- function(v) data.frame(year = YEARS, value = v)

FB <- list(
  # A4002E1A156NBEA — Compensation of employees / GDI
  comp = .fb(c(
    58.4,57.6,57.5,57.3,57.7,56.7,56.6,56.5,56.6,57.2,
    57.7,56.6,56.8,56.3,55.5,55.7,56.5,56.6,56.3,56.4,
    57.0,56.9,57.3,57.0,56.1,55.7,55.2,55.0,55.7,56.0,
    56.6,56.5,55.8,55.4,55.0,54.0,53.4,54.6,55.3,54.4,
    53.0,52.7,52.3,52.3,52.2,52.8,53.2,53.4,53.3,53.3,
    54.6,53.1,51.7,51.8,51.9)),
  # A262RE1A156NBEA — Consumption of fixed capital (depreciation) / GDI
  dep = .fb(c(
    12.8,12.9,12.7,12.6,13.5,14.3,14.0,14.1,14.1,14.5,
    15.2,15.4,16.1,15.7,15.0,14.9,15.2,15.2,15.0,15.0,
    15.1,15.4,15.0,15.0,14.8,14.9,14.7,14.5,14.4,14.5,
    14.6,15.0,15.1,15.0,14.9,15.1,15.1,15.6,16.2,16.6,
    16.0,15.8,15.7,15.9,15.9,15.9,16.0,16.1,16.1,16.2,
    17.0,16.3,16.5,16.6,16.5)),
  # A041RE1A156NBEA — Proprietors' income / GDI
  prop = .fb(c(
    7.3,7.3,7.5,7.9,7.3,7.1,7.1,7.0,7.1,6.9,
    6.1,5.7,5.1,5.2,5.7,5.6,5.7,6.0,6.2,6.1,
    6.0,5.8,6.2,6.4,6.4,6.4,6.8,6.8,7.0,7.2,
    7.3,7.8,7.9,7.8,7.9,7.5,7.5,6.9,6.6,6.6,
    7.4,7.9,7.9,8.0,7.7,7.3,7.2,7.3,7.3,7.2,
    7.5,7.7,7.2,7.1,7.0)),
  # W270RE1A156NBEA — Wages & salaries / GDI
  wages = .fb(c(
    51.6,50.6,50.2,49.9,50.2,48.7,48.5,48.2,48.1,48.5,
    48.8,47.7,47.6,46.9,46.2,46.3,46.7,46.9,46.6,46.3,
    46.7,46.4,46.3,45.9,45.3,45.3,45.1,45.2,45.8,46.1,
    46.6,46.3,45.3,44.7,44.2,43.4,43.1,44.2,44.8,43.7,
    42.5,42.4,42.2,42.0,42.1,42.7,43.1,43.3,43.2,43.4,
    44.5,43.5,42.7,42.7,42.7)),
  # A445RE1A156NBEA — Corporate profits w/ IVA+CCAdj (pre-tax) / GDI
  corp_pre = .fb(c(
    7.4,7.6,8.0,8.8,7.0,7.2,8.0,8.2,8.3,7.9,
    6.2,6.6,5.3,5.9,6.7,6.2,5.8,6.4,6.8,6.5,
    6.0,5.8,5.7,6.4,7.1,8.0,8.2,8.3,7.6,7.5,
    7.3,6.6,6.8,7.5,8.6,9.6,10.2,8.2,6.9,8.2,
    9.6,9.6,10.2,10.2,10.0,9.3,9.1,9.4,9.4,9.5,
    9.3,11.4,11.2,11.4,11.5)),
  # W273RE1A156NBEA — Corporate profits w/ IVA+CCAdj (after-tax) / GDI
  corp_post = .fb(c(
    4.7,4.9,5.2,5.8,4.2,4.4,5.1,5.3,5.4,4.9,
    3.8,4.2,3.2,3.9,4.5,4.0,3.6,4.3,4.7,4.4,
    4.0,3.8,3.8,4.4,5.1,5.9,6.1,6.3,5.7,5.6,
    5.4,4.6,4.9,5.7,6.8,7.7,8.2,6.3,5.0,6.5,
    7.7,7.6,8.2,8.2,7.9,7.3,7.2,7.5,7.5,7.6,
    7.8,9.4,8.9,9.2,9.2)),
  # Taxes on production & imports less subsidies / GDI
  # (no clean FRED share series; original hardcoded this — kept static)
  taxes = .fb(c(
    7.0,6.9,6.9,6.7,7.2,7.2,7.1,6.9,6.8,6.7,
    6.8,7.0,7.0,7.0,6.9,6.8,6.6,6.6,6.5,6.4,
    6.4,6.6,6.6,6.6,6.6,6.6,6.5,6.4,6.5,6.4,
    6.3,6.3,6.5,6.5,6.5,6.6,6.6,6.6,6.3,6.1,
    6.3,6.4,6.5,6.4,6.4,6.5,6.5,6.5,6.5,6.6,
    6.4,6.4,6.5,6.6,6.7))
)

# LABSHPUSA156NRUG — Penn World Table labor share (1970–2019 only)
PWT_YEARS <- 1970:2019
FB_PWT <- data.frame(year = PWT_YEARS, value = 100 * c(
  0.6490,0.6376,0.6394,0.6407,0.6410,0.6256,0.6216,0.6216,0.6223,0.6226,
  0.6243,0.6142,0.6167,0.6039,0.6020,0.6023,0.6077,0.6160,0.6207,0.6119,
  0.6152,0.6151,0.6200,0.6142,0.6080,0.6074,0.6071,0.6096,0.6230,0.6260,
  0.6371,0.6403,0.6296,0.6214,0.6171,0.6056,0.6055,0.6040,0.6041,0.5911,
  0.5880,0.5927,0.5951,0.5931,0.5943,0.5956,0.5938,0.5962,0.5943,0.5971))

# Employer FICA statutory rates (OASDI + Medicare, %), for modeled series
FICA_RATES <- c(
  `1970`=4.80,`1971`=5.20,`1972`=5.20,`1973`=5.85,`1974`=5.85,
  `1975`=5.85,`1976`=5.85,`1977`=5.85,`1978`=6.05,`1979`=6.13,
  `1980`=6.13,`1981`=6.65,`1982`=6.70,`1983`=6.70,`1984`=7.00,
  `1985`=7.05,`1986`=7.15,`1987`=7.15,`1988`=7.51,`1989`=7.51)
FICA_RATES[as.character(1990:2024)] <- 7.65
WAGE_CAP_ADJUSTMENT <- 0.91   # calibrated to 2024 actual ($866B / $29,002B GDI = 2.99%)

# Figure 3 static series (corporate profits WITHOUT IVA/CCAdj, 5-yr points)
# From generate_capital_share_chart.py; A053RC1A027NBEA / A055RC1A027NBEA / GDIA.
F3_YEARS      <- c(1970,1975,1980,1985,1990,1995,2000,2005,2010,2015,2020,2024)
FB_F3_PRE     <- c(8.1,7.5,7.2,7.4,6.8,8.5,8.3,10.5,10.8,11.5,11.0,14.4)
FB_F3_POST    <- c(5.2,4.5,4.5,4.8,4.5,6.2,5.8, 8.2, 8.6, 9.5, 9.0,12.1)
FB_F3_PROP    <- c(7.8,6.9,6.2,6.6,7.0,7.4,7.6, 8.4, 7.6, 7.4, 7.5, 7.0)

# 1929 historical reference
HIST_1929 <- list(compensation = 49.5, depreciation = 10.0,
                  proprietors = 13.5, wages = 48.6)

# =====================================================================
# build_dataset() — fetch (or fall back), align by year, derive measures
# =====================================================================
build_dataset <- function() {
  api_key <- Sys.getenv("FRED_API_KEY", "")
  mode <- if (nzchar(api_key)) "LIVE FRED API" else "STATIC fallback (no FRED_API_KEY)"
  message("Data source mode: ", mode)

  # core annual share series -----------------------------------------
  s_comp  <- get_series("A4002E1A156NBEA", FB$comp,  api_key, "Compensation/GDI")
  s_dep   <- get_series("A262RE1A156NBEA", FB$dep,   api_key, "Depreciation/GDI")
  s_prop  <- get_series("A041RE1A156NBEA", FB$prop,  api_key, "Proprietors'/GDI")
  s_wages <- get_series("W270RE1A156NBEA", FB$wages, api_key, "Wages/GDI")
  s_cpre  <- get_series("A445RE1A156NBEA", FB$corp_pre,  api_key, "Corp profits pre-tax/GDI")
  s_cpost <- get_series("W273RE1A156NBEA", FB$corp_post, api_key, "Corp profits post-tax/GDI")
  s_pwt   <- get_series("LABSHPUSA156NRUG", FB_PWT, api_key, "PWT labor share",
                        obs_start = "1970-01-01", obs_end = "2019-12-31")
  # taxes on production kept static (no clean FRED share series)
  s_tax   <- list(src = "static", data = FB$taxes)

  srcs <- c(comp=s_comp$src, dep=s_dep$src, prop=s_prop$src, wages=s_wages$src,
            corp_pre=s_cpre$src, corp_post=s_cpost$src, pwt=s_pwt$src, taxes=s_tax$src)

  pull <- function(s) s$data$value[match(YEARS, s$data$year)]

  df <- data.frame(
    year      = YEARS,
    comp      = pull(s_comp),
    dep       = pull(s_dep),
    prop      = pull(s_prop),
    wages     = pull(s_wages),
    corp_pre  = pull(s_cpre),
    corp_post = pull(s_cpost),
    taxes     = pull(s_tax)
  )
  df$pwt <- FB_PWT$value[match(YEARS, PWT_YEARS)]
  if (identical(s_pwt$src, "live"))
    df$pwt <- s_pwt$data$value[match(YEARS, s_pwt$data$year)]

  # --- derived measures (identical formulas to generate_chart.py) ----
  df$net_labor      <- df$comp / (100 - df$dep) * 100
  df$adj_labor      <- df$comp + 0.67 * df$prop
  df$supplements    <- df$comp - df$wages

  rate <- FICA_RATES[as.character(df$year)] / 100
  df$fica_share     <- rate * df$wages * WAGE_CAP_ADJUSTMENT   # % of GDI
  df$comp_ex_fica   <- df$comp - df$fica_share

  df$nos_raw        <- 100 - df$comp - df$dep - df$taxes
  df$nos            <- df$nos_raw - (2/3) * df$prop
  df$corp_tax       <- df$corp_pre - df$corp_post
  df$nos_aftertax   <- df$nos - df$corp_tax
  df$corp_adjusted  <- df$corp_pre + (1/3) * df$prop
  df$nos_depr_adj   <- df$nos / (100 - df$dep) * 100

  # --- Figure 3 (corporate profit share, without IVA/CCAdj) ----------
  # Static fallback = published 5-yr points; live = annual A053RC/A055RC / GDIA.
  f3 <- build_figure3(api_key)

  list(df = df, f3 = f3, srcs = srcs, mode = mode)
}

build_figure3 <- function(api_key) {
  if (nzchar(api_key)) {
    ok <- TRUE
    fetch <- function(id) tryCatch(fred_get(id, api_key), error = function(e) {ok<<-FALSE; NULL})
    pre_lvl  <- fetch("A053RC1A027NBEA")   # corp profits before tax, w/o IVA&CCAdj ($B)
    post_lvl <- fetch("A055RC1A027NBEA")   # corp profits after tax,  w/o IVA&CCAdj ($B)
    gdi_lvl  <- fetch("GDIA")              # gross domestic income ($B, annual)
    prop_sh  <- fetch("A041RE1A156NBEA")   # proprietors' income / GDI (%)
    if (ok && !is.null(pre_lvl) && !is.null(gdi_lvl)) {
      yrs <- gdi_lvl$year
      al  <- function(x) x$value[match(yrs, x$year)]
      pre  <- al(pre_lvl)  / al(gdi_lvl) * 100
      post <- al(post_lvl) / al(gdi_lvl) * 100
      prop <- al(prop_sh)
      message(sprintf("  [ LIVE ] Figure 3 computed from levels (%d yrs)", length(yrs)))
      return(data.frame(year = yrs,
                        pretax_adj  = pre  + (1/3) * prop,
                        posttax_adj = post + (1/3) * prop))
    }
    message("  [static] Figure 3 (live level fetch failed; using published points)")
  } else {
    message("  [static] Figure 3 (published 5-yr points)")
  }
  data.frame(year = F3_YEARS,
             pretax_adj  = FB_F3_PRE  + (1/3) * FB_F3_PROP,
             posttax_adj = FB_F3_POST + (1/3) * FB_F3_PROP)
}
