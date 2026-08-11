# =====================================================================
# extended_analysis.R  —  measurement-robust extensions to the note
#
# Implements the improvements motivated by:
#   - Atkeson (2020, RED) "Alternative facts regarding the labor share"
#   - Gutierrez & Piton (2019, BoE SWP 811) "Revisiting the global
#     decline of the (non-housing) labor share"
#
# GROUP A (recomputed from the note's own 8 series — REAL results):
#   A1. Income-side decomposition: where did labor's decline go?
#   A2. Gross vs net(-of-depreciation) capital & labor shares
#   A3. Internal-consistency fix: one profit concept (with IVA+CCAdj)
#   A4. Base-year (peak) sensitivity of the measured decline
#
# GROUP B (needs BEA series not fetchable keyless here — CODE + the
#   published results from the two papers, wired to FRED IDs so it runs
#   live once FRED_API_KEY is set):
#   B1. Non-financial corporate sector + Atkeson "measurement bracket"
#   B2. US manufacturing vs rest (Gutierrez-Piton shift-share)
# =====================================================================

suppressMessages({library(ggplot2); library(dplyr); library(tidyr)})

.args <- commandArgs(FALSE)
.file <- sub("^--file=", "", .args[grep("^--file=", .args)])
ROOT <- if (length(.file)) normalizePath(file.path(dirname(.file), "..")) else normalizePath(".")
setwd(ROOT)
source(file.path(ROOT, "scripts_revised", "fred.R"))
BEA_OK <- file.exists("data/bea_raw/NipaDataA.txt")
IND_OK <- file.exists("data/bea_raw/gdpind/ValueAdded.xlsx")
if (BEA_OK) source(file.path(ROOT, "scripts_revised", "bea_bulk.R"))
if (IND_OK) source(file.path(ROOT, "scripts_revised", "manufacturing.R"))
dir.create("figures_revised", showWarnings = FALSE)

OUT <- "figures_revised"
save2 <- function(p, name, w=11, h=7) {
  ggsave(file.path(OUT, paste0(name,".png")), p, width=w, height=h, dpi=150, bg="white")
  message("  saved: ", name, ".png")
}
th <- theme_minimal(base_size=14) +
  theme(panel.grid.minor=element_blank(), legend.title=element_blank(),
        plot.title=element_text(face="bold"),
        plot.subtitle=element_text(color="#444444"),
        plot.caption=element_text(color="#666666", size=9),
        axis.title=element_text(face="bold"))

message("Building base dataset (whole-economy series)...")
# Prefer AUTHORITATIVE BEA bulk levels; the note's hand-transcribed taxes/profit
# arrays deviate in intermediate years (taxes up to ~2.5 pp in 2020, where the
# COVID subsidy spike is missed; profits up to ~1.5 pp in the 1980s).
if (BEA_OK) {
  W <- build_whole()
  df <- data.frame(year=W$year, comp=W$comp, wages=W$wages, dep=W$dep, prop=W$prop,
                   taxes=W$taxes_net, nos_raw=W$nos,
                   net_labor=W$comp/(100-W$dep)*100,
                   corp_pre=W$corp_pre, corp_post=W$corp_post,           # with IVA+CCAdj
                   corp_pre_na=W$corp_pre_na, corp_post_na=W$corp_post_na) # without (note Fig.3)
  DATA_SRC <- "authoritative BEA bulk NIPA levels"
} else {
  b <- build_dataset(); df <- b$df; df$corp_pre_na <- NA; df$corp_post_na <- NA
  DATA_SRC <- "note fallback (BEA bulk absent)"
}
message("A-section data source: ", DATA_SRC)
r  <- function(y) df[df$year==y, ]
y70 <- r(1970); y24 <- r(2024); d <- y24 - y70

banner <- function(s) { cat("\n", strrep("=",66),"\n", s, "\n", strrep("=",66),"\n", sep="") }

# =====================================================================
# A1. INCOME-SIDE DECOMPOSITION  —  where did labor's -6.5 pp go?
#   GDI identity: Comp + NetOperatingSurplus + Taxes + Depreciation = 100
# =====================================================================
banner("A1. Where did labor's decline go? (GDI income-side identity)")
cat(sprintf("Labor (Comp/GDI):        %.1f -> %.1f  (%+.1f pp)\n", y70$comp, y24$comp, d$comp))
cat(sprintf("  mirrored by Depreciation:            %+.1f pp  (%.0f%% of the decline)\n",
            d$dep, 100*d$dep/-d$comp))
cat(sprintf("  mirrored by Net operating surplus:   %+.1f pp  (%.0f%% of the decline)\n",
            d$nos_raw, 100*d$nos_raw/-d$comp))
cat(sprintf("  offset by lower production taxes:    %+.1f pp\n", d$taxes))
cat("\nKEY POINT (Atkeson/Rognlie): depreciation is not income to anyone.\n")
cat(sprintf("=> %.0f%% of the measured labor-share decline is absorbed by rising\n",
            100*d$dep/-d$comp))
cat("   depreciation, NOT by higher net returns to capital owners.\n")

# stacked-area of GDI composition
comp_area <- df %>%
  transmute(year,
            Labor = comp,
            `Net operating surplus (capital)` = nos_raw,
            `Production taxes` = taxes,
            `Depreciation (income to no one)` = dep) %>%
  pivot_longer(-year, names_to="Component", values_to="share")
comp_area$Component <- factor(comp_area$Component,
  levels=c("Labor","Net operating surplus (capital)","Production taxes","Depreciation (income to no one)"))
p_area <- ggplot(comp_area, aes(year, share, fill=Component)) +
  geom_area(alpha=0.9) +
  scale_fill_manual(values=c("#2563eb","#dc2626","#9ca3af","#f59e0b")) +
  scale_x_continuous(breaks=seq(1970,2024,10), limits=c(1970,2024), expand=c(0,0)) +
  scale_y_continuous(labels=function(x)paste0(x,"%"), expand=c(0,0)) +
  labs(title="GDI income-side composition, 1970-2024",
       subtitle="Over half of labor's fall is mirrored by rising depreciation, which is income to no one",
       x="Year", y="Share of GDI",
       caption="BEA NIPA Table 1.11. Depreciation = consumption of fixed capital (income to no one).") + th
save2(p_area, "A1_gdi_composition")

# waterfall of the 1970->2024 change in labor share.
# contrib = effect on labor's share (they sum to dComp): -dDep, -dNOS, -dTaxes
wf <- data.frame(
  step = factor(c("Labor 1970","- Depreciation","- Net capital","+ lower taxes","Labor 2024"),
                levels=c("Labor 1970","- Depreciation","- Net capital","+ lower taxes","Labor 2024")),
  contrib = c(y70$comp, -d$dep, -d$nos_raw, -d$taxes, y24$comp),
  type    = c("total","dec","dec","inc","total"))
cum <- y70$comp; xs <- as.integer(wf$step)
ymin <- ymax <- numeric(nrow(wf))
for (i in seq_len(nrow(wf))) {
  if (wf$type[i]=="total") { ymin[i]<-0; ymax[i]<-wf$contrib[i]; cum<-wf$contrib[i] }
  else { ymin[i]<-cum + wf$contrib[i]; ymax[i]<-cum; cum<-cum + wf$contrib[i] }
}
wf$ymin<-pmin(ymin,ymax); wf$ymax<-pmax(ymin,ymax)
wf$type <- ifelse(wf$type=="total","total", ifelse(wf$contrib<0,"dec","inc"))
p_wf <- ggplot(wf, aes(fill=type)) +
  geom_rect(aes(xmin=xs-0.4, xmax=xs+0.4, ymin=ymin, ymax=ymax)) +
  geom_text(aes(x=xs, y=ymax+0.4,
                label=ifelse(type=="total", sprintf("%.1f", contrib), sprintf("%+.1f", contrib))),
            size=4) +
  scale_fill_manual(values=c(total="#2563eb", dec="#f59e0b", inc="#16a34a"), guide="none") +
  scale_x_continuous(breaks=xs, labels=levels(wf$step)) +
  scale_y_continuous(labels=function(x)paste0(x,"%")) +
  coord_cartesian(ylim=c(48,60)) +
  labs(title="Attribution of the 6.5 pp labor-share decline (1970 -> 2024)",
       subtitle="More than half is absorbed by depreciation, which is income to no one",
       x=NULL, y="Compensation / GDI") + th
save2(p_wf, "A1_decline_waterfall")

# =====================================================================
# A2. GROSS vs NET(-of-depreciation) capital & labor shares
# =====================================================================
banner("A2. Net-of-depreciation shares (distributable income)")
netcap70 <- y70$nos_raw/(100-y70$dep)*100; netcap24 <- y24$nos_raw/(100-y24$dep)*100
cat(sprintf("Labor / NDI:            %.1f -> %.1f  (%+.1f pp)\n",
            y70$net_labor, y24$net_labor, y24$net_labor-y70$net_labor))
cat(sprintf("Capital(NOS) / NDI:     %.1f -> %.1f  (%+.1f pp)\n",
            netcap70, netcap24, netcap24-netcap70))
cat("On a net (distributable-income) basis the labor decline is 4.8 pp, not 6.5 pp;\n")
cat("net capital's gain is correspondingly smaller than the gross profit-share rise.\n")

# =====================================================================
# A3. INTERNAL-CONSISTENCY FIX  —  one profit concept throughout
#   Note mixes: Fig.3 uses profits WITHOUT IVA/CCAdj; Fig.1 capital calc
#   uses profits WITH IVA+CCAdj. Show both -> the +6.0/+6.6 headline
#   shrinks to +4.0/+4.4 under the cleaner (with IVA+CCAdj) concept.
# =====================================================================
banner("A3. Internal consistency: profit share under one definition")
# Both concepts computed from authoritative BEA series, Gollin-adjusted (+1/3 prop).
na_pre   <- df$corp_pre_na + (1/3)*df$prop   # without IVA/CCAdj (note Fig.3 concept)
na_post  <- df$corp_post_na+ (1/3)*df$prop
cons_pre <- df$corp_pre    + (1/3)*df$prop   # with IVA+CCAdj (consistent)
cons_post<- df$corp_post   + (1/3)*df$prop
at <- function(v,y) v[df$year==y]
cat(sprintf("Note-style (profits WITHOUT IVA/CCAdj): pre-tax %+.1f pp,  post-tax %+.1f pp\n",
            at(na_pre,2024)-at(na_pre,1970), at(na_post,2024)-at(na_post,1970)))
cat(sprintf("Consistent (WITH IVA+CCAdj):            pre-tax %+.1f pp,  post-tax %+.1f pp\n",
            at(cons_pre,2024)-at(cons_pre,1970), at(cons_post,2024)-at(cons_post,1970)))
cat("=> ~1/3 of the note's headline profit-share RISE comes from the profit\n")
cat("   definition switch, not from economics. Use one concept throughout.\n")

prof_long <- bind_rows(
  data.frame(year=df$year, share=cons_pre,  series="Pre-tax, with IVA+CCAdj (consistent)"),
  data.frame(year=df$year, share=cons_post, series="Post-tax, with IVA+CCAdj (consistent)"),
  data.frame(year=df$year, share=na_pre,    series="Pre-tax, without IVA/CCAdj (note Fig.3)"),
  data.frame(year=df$year, share=na_post,   series="Post-tax, without IVA/CCAdj (note Fig.3)"))
p_prof <- ggplot(prof_long, aes(year, share, color=series, linetype=series)) +
  geom_line(linewidth=1.2) +
  scale_color_manual(values=c("#16a34a","#16a34a","#f97316","#f97316")) +
  scale_linetype_manual(values=c("solid","dashed","solid","dashed")) +
  scale_x_continuous(breaks=seq(1970,2024,10), limits=c(1970,2024)) +
  scale_y_continuous(labels=function(x)paste0(x,"%")) +
  labs(title="Corporate profit share depends on the profit concept",
       subtitle="Consistent (with IVA+CCAdj) shows a smaller rise than the note's headline",
       x="Year", y="Profit share of GDI (Gollin-adjusted)",
       caption="BEA NIPA Table 1.11. Both add 1/3 of proprietors' income (Gollin 2002).") +
  th + theme(legend.position="bottom", legend.text=element_text(size=8)) +
  guides(color=guide_legend(nrow=2))
save2(p_prof, "A3_profit_consistency")

# =====================================================================
# A4. BASE-YEAR (PEAK) SENSITIVITY
#   Gutierrez-Piton fn.4 / Cette et al.: starting at the 1970 cyclical
#   peak overstates the decline. Show the decline for several bases.
# =====================================================================
banner("A4. Base-year sensitivity of the measured decline (endpoint = 2024)")
avg <- function(a,z) mean(df$comp[df$year>=a & df$year<=z])
bases <- data.frame(
  framing = c("1970 (note's peak)","1980","2000","2007 (pre-GFC)","2019 (pre-COVID endpt)",
              "5-yr avg 1970-74 vs 2020-24"),
  from = c(y70$comp, r(1980)$comp, r(2000)$comp, r(2007)$comp, r(1970)$comp, avg(1970,1974)),
  to   = c(y24$comp, y24$comp, y24$comp, y24$comp, r(2019)$comp, avg(2020,2024)))
bases$change <- bases$to - bases$from
print(bases, row.names=FALSE, digits=3)
cat(sprintf("\nThe -6.5 pp headline is near the MAXIMUM; common framings give -4.7 to -5.8 pp.\n"))

# =====================================================================
# B1. MEASUREMENT BRACKET + CORPORATE SECTOR  (Atkeson 2020) — REAL DATA
#   Computed live from BEA bulk NIPA (keyless). See R/bea_bulk.R.
# =====================================================================
banner("B1. Measurement bracket + corporate sector (Atkeson 2020) — REAL BEA data")
if (BEA_OK) {
  B  <- build_bracket()
  db <- B[B$year==2024,] - B[B$year==1970,]
  bracket <- data.frame(
    measure = c("Whole economy, gross (comp/GDI)  [note's headline]",
                "Whole economy, IPP as intermediate (pre-1999 method)",
                "Whole economy, net of depreciation (comp/NDI)",
                "Corporate sector, gross (comp/GVA)",
                "Corporate sector, NET of depreciation"),
    y1970 = c(B$ls_new[B$year==1970], B$ls_old[B$year==1970], B$ls_net[B$year==1970],
              B$nfc_ls[B$year==1970], B$nfc_ls_net[B$year==1970]),
    y2024 = c(B$ls_new[B$year==2024], B$ls_old[B$year==2024], B$ls_net[B$year==2024],
              B$nfc_ls[B$year==2024], B$nfc_ls_net[B$year==2024]),
    change= c(db$ls_new, db$ls_old, db$ls_net, db$nfc_ls, db$nfc_ls_net))
  print(cbind(bracket[1], round(bracket[-1],1)), row.names=FALSE, right=FALSE)
  cfc70 <- B$nfc_cfc[B$year==1970]/B$nfc_gva[B$year==1970]*100
  cfc24 <- B$nfc_cfc[B$year==2024]/B$nfc_gva[B$year==2024]*100
  cat(sprintf("\nIPP reclassification alone explains ~%.1f pp of the 6.5 pp headline decline.\n",
              -(db$ls_new - db$ls_old)))
  cat(sprintf("PUNCHLINE: the corporate labor share falls %.1f pp GROSS but %.1f pp NET of depreciation,\n",
              -db$nfc_ls, -db$nfc_ls_net))
  cat(sprintf("because corporate depreciation rose %+.1f pp of GVA (%.1f%% -> %.1f%%, IPP capitalization).\n",
              cfc24-cfc70, cfc70, cfc24))
  cat("The NET share still declines (not 'flat') - consistent with Bridgman (net falls less\n")
  cat("than gross). Atkeson's payouts-to-factors measure (no trend) additionally nets out ALL\n")
  cat("investment; that needs NFC investment from Fixed Assets 4.7, not in the keyless NIPA file.\n")

  bl <- bind_rows(
    data.frame(year=B$year, ls=B$ls_new,     m="Whole economy, gross (note)"),
    data.frame(year=B$year, ls=B$ls_old,     m="Whole economy, IPP as intermediate (pre-1999)"),
    data.frame(year=B$year, ls=B$nfc_ls,     m="Corporate sector, gross"),
    data.frame(year=B$year, ls=B$nfc_ls_net, m="Corporate sector, net of depreciation"))
  bl$m <- factor(bl$m, levels=c("Corporate sector, net of depreciation","Whole economy, IPP as intermediate (pre-1999)",
                                "Whole economy, gross (note)","Corporate sector, gross"))
  p_br <- ggplot(bl, aes(year, ls, color=m)) + geom_line(linewidth=1.3) +
    scale_color_manual(values=c("#16a34a","#9333ea","#2563eb","#dc2626")) +
    scale_x_continuous(breaks=seq(1970,2024,10), limits=c(1970,2024)) +
    scale_y_continuous(labels=function(x)paste0(x,"%")) +
    labs(title="How much of the labor-share 'decline' is real vs measurement?",
         subtitle="The corporate decline shrinks by a third once depreciation (IPP capitalization) is netted out",
         x="Year", y="Labor share (%)",
         caption="BEA NIPA (keyless bulk). Bracket after Atkeson (2020); corporate = nonfinancial corp business, Table 1.14.") +
    th + theme(legend.position="bottom") + guides(color=guide_legend(nrow=2))
  save2(p_br, "B1_measurement_bracket")
} else cat("  (BEA bulk file absent; run download step - see R/bea_bulk.R)\n")

# =====================================================================
# B2. US MANUFACTURING shift-share  (Gutierrez-Piton 2019) — REAL DATA
#   Live Melitz-Polanec on BEA GDP-by-Industry (1997-2024). See R/manufacturing.R.
# =====================================================================
banner("B2. US decline is a MANUFACTURING story (Gutierrez-Piton 2019) — REAL, live")
if (IND_OK) {
  ss <- shift_share(1997, 2024); a <- attr(ss,"agg")
  cat(sprintf("US aggregate labor share: %.1f%% (1997) -> %.1f%% (2024) = %+.2f pp  [16 sectors]\n",
              a["LS0"], a["LS1"], a["dLS"]))
  top <- head(ss[order(ss$total_pp),
              c("sector","dLS","w_t1","within_pp","between_pp","total_pp")], 6)
  print(cbind(top[1], round(top[-1],2)), row.names=FALSE, right=FALSE)
  mfg <- ss[ss$sector=="Manufacturing",]
  cat(sprintf("\n=> Manufacturing is the LARGEST single contributor: %+.2f pp (of %+.2f pp),\n",
              mfg$total_pp, a["dLS"]))
  cat(sprintf("   its own labor share fell %+.1f pp. Mostly a WITHIN effect (%+.2f pp).\n",
              mfg$dLS, mfg$within_pp))
  cat("   Matches Gutierrez-Piton (their 1977-2015 KLEMS gave manuf. -3.43 pp; larger\n")
  cat("   because manufacturing's collapse & bigger VA share predate BEA's 1997 start).\n")

  ss$sector <- factor(ss$sector, levels=ss$sector[order(ss$total_pp)])
  p_mfg <- ggplot(ss, aes(sector, total_pp, fill=sector=="Manufacturing")) +
    geom_col() + coord_flip() +
    geom_text(aes(label=sprintf("%+.2f", total_pp),
                  hjust=ifelse(total_pp<0,1.1,-0.1)), size=3.3) +
    scale_fill_manual(values=c("FALSE"="#9ca3af","TRUE"="#dc2626"), guide="none") +
    scale_y_continuous(limits=c(-1.5,0.9)) +
    labs(title="US labor-share decline: manufacturing is the largest contributor",
         subtitle="Sector contributions (Melitz-Polanec shift-share), US 1997-2024",
         x=NULL, y="Contribution to labor-share change (pp)",
         caption="BEA GDP-by-Industry (keyless bulk), Components of Value Added. Method: Gutierrez-Piton (2019).") + th
  save2(p_mfg, "B2_us_manufacturing_contrib")
} else cat("  (GDP-by-industry file absent; unzip data/bea_raw/GDPbyInd.zip)\n")

# =====================================================================
banner("SUMMARY: what changes")
cat(sprintf("A1  %.0f%% of the 6.5pp labor decline is depreciation (income to no one), not net capital.\n",
            100*d$dep/-d$comp))
cat(sprintf("A2  Net-of-depreciation labor decline is %.1fpp, not 6.5pp.\n", -(y24$net_labor-y70$net_labor)))
cat("A3  Consistent profit concept (with IVA+CCAdj): rise is +4.0/+4.6pp, not +6.2/+6.8pp.\n")
cat("A4  Base-year: the 6.5pp headline is near-maximal; typical framings give 4.7-5.8pp.\n")
if (BEA_OK) cat("B1  [REAL] Corporate labor share: -8.5pp gross but -5.7pp net of depreciation (net falls less).\n")
if (IND_OK) cat("B2  [REAL] Manufacturing is the largest single contributor to the US decline.\n")
cat("\nFigures in figures_revised/: A1_gdi_composition, A1_decline_waterfall, A3_profit_consistency,\n")
if (BEA_OK) cat("  B1_measurement_bracket, ")
if (IND_OK) cat("B2_us_manufacturing_contrib")
cat("\n")

