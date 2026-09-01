"""Verify all checkable references of RRHM v6 against live PubMed esummary and CrossRef.

Field-by-field: title, first author, journal, year, volume, pages, DOI.
Zero-vs-unresolved discipline: an unreachable/unindexed entry is UNRESOLVED, never 'wrong'.
"""
import json, time, urllib.request, urllib.parse, re, difflib

UA = {'User-Agent': 'ref-verify/1.0 (mailto:arayawedding@gmail.com)'}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())

def norm(s):
    if s is None: return ''
    s = s.lower().replace('–','-').replace('—','-')
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()

def tsim(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()

# id, pmid, doi, first_author_last, title, journal_abbrev, year, volume, pages
REFS = [
 (1, '28222820', '10.1017/S0033291717000174', 'Wardenaar', 'The cross-national epidemiology of specific phobia in the World Mental Health Surveys', 'Psychol Med', 2017, '47', '1744-1760'),
 (2, None, '10.1017/S0033291717002975', 'Wardenaar', 'The cross-national epidemiology of specific phobia in the World Mental Health Surveys - CORRIGENDUM', 'Psychol Med', 2018, '48', '878-879'),
 (3, '36323055', '10.1016/j.brat.2022.104203', 'Odgers', 'The relative efficacy and efficiency of single- and multi-session exposure therapies for specific phobia: A meta-analysis', 'Behav Res Ther', 2022, '159', '104203'),
 (4, '19815371', '10.1016/j.janxdis.2009.09.002', 'Trumpf', 'Incidence and predictors of specific phobia in young women: a prospective community study', 'J Anxiety Disord', 2010, '24', '87-93'),
 (5, '19604666', '10.1016/j.janxdis.2009.06.005', 'Trumpf', 'Rates and predictors of remission in young women with specific phobia: a prospective community study', 'J Anxiety Disord', 2009, '23', '958-964'),
 (6, '31830494', None, 'Bohnlein', 'Factors influencing the success of exposure therapy for specific phobia: A systematic review', 'Neurosci Biobehav Rev', 2020, '108', '796-820'),
 (7, '39889926', '10.1016/j.jad.2025.01.133', 'de Vos', 'Long-term exposure therapy outcome in phobia and the link with behavioral and neural indices of extinction learning', 'J Affect Disord', 2025, '375', '324-330'),
 (8, '26257618', None, 'Krypotos', 'Avoidance learning: a review of theoretical models and recent developments', 'Front Behav Neurosci', 2015, '9', '189'),
 (9, '29550209', None, 'Pittig', 'The role of associative fear and avoidance learning in anxiety disorders: gaps and directions for future research', 'Neurosci Biobehav Rev', 2018, '88', '117-140'),
 (10, '24864005', None, 'Craske', 'Maximizing exposure therapy: an inhibitory learning approach', 'Behav Res Ther', 2014, '58', '10-23'),
 (11, '39706234', '10.1016/j.neubiorev.2024.105983', 'Kausche', 'Fear and safety learning in anxiety- and stress-related disorders: an updated meta-analysis', 'Neurosci Biobehav Rev', 2025, '169', '105983'),
 (12, '17717184', None, 'Mobbs', 'When fear is near: threat imminence elicits prefrontal-periaqueductal gray shifts in humans', 'Science', 2007, '317', '1079-1083'),
 (13, None, '10.1016/j.tics.2019.12.016', 'Mobbs', 'Space, time, and fear: survival computations along defensive circuits', 'Trends Cogn Sci', 2020, '24', '228-241'),
 (14, None, '10.1073/pnas.1712314115', 'Qi', 'How cognitive and reactive fear circuits optimize escape decisions in humans', 'Proc Natl Acad Sci USA', 2018, '115', '3186-3191'),
 (15, None, '10.1038/s41467-025-60666-9', 'Zhang', 'An intracranial dissection of human escape circuits', 'Nat Commun', 2025, '16', '5520'),
 (16, '31110337', '10.1038/s41562-019-0595-5', 'Fung', 'Slow escape decisions are swayed by trait anxiety', 'Nat Hum Behav', 2019, '3', '702-708'),
 (17, '27337390', '10.1037/rev0000033', 'Maier', 'Learned helplessness at fifty: insights from neuroscience', 'Psychol Rev', 2016, '123', '349-367'),
 (18, '24333646', None, 'Hartley', 'Stressor controllability modulates fear extinction in humans', 'Neurobiol Learn Mem', 2014, '113', '149-156'),
 (19, '26149910', None, 'Wood', 'Controllability modulates the neural response to predictable but not unpredictable threat in humans', 'Neuroimage', 2015, '119', '371-381'),
 (20, '18023604', None, 'Droit-Volet', 'How emotions colour our perception of time', 'Trends Cogn Sci', 2007, '11', '504-513'),
 (21, '18074019', None, 'Stetson', 'Does time really slow down during a frightening event?', 'PLoS One', 2007, '2', 'e1295'),
 (22, '27895566', None, 'Stephan', 'Allostatic self-efficacy: a metacognitive theory of dyshomeostasis-induced fatigue and depression', 'Front Hum Neurosci', 2016, '10', '550'),
 (23, '31067416', None, 'Paulus', 'An active inference approach to interoceptive psychopathology', 'Annu Rev Clin Psychol', 2019, '15', '97-122'),
 (24, '27609244', None, 'LeDoux', 'Using neuroscience to help understand fear and anxiety: a two-system framework', 'Am J Psychiatry', 2016, '173', '1083-1093'),
 (25, '8466392', None, 'Klein', 'False suffocation alarms, spontaneous panics, and related conditions: an integrative hypothesis', 'Arch Gen Psychiatry', 1993, '50', '306-317'),
 (26, '19464700', None, 'Ayala', 'Treatments for blood-injury-injection phobia: a critical review of current evidence', 'J Psychiatr Res', 2009, '43', '1235-1242'),
 (27, '3593159', None, 'Ost', 'Applied tension: a specific behavioral method for treatment of blood phobia', 'Behav Res Ther', 1987, '25', '25-29'),
 (28, '20576505', None, 'Ritz', 'The psychophysiology of blood-injection-injury phobia: looking beyond the diphasic response paradigm', 'Int J Psychophysiol', 2010, '78', '50-67'),
 (29, '32444982', None, 'Huppert', 'Acrophobia and visual height intolerance: advances in epidemiology and mechanisms', 'J Neurol', 2020, '267', '231-240'),
 (30, '39128857', '10.1111/jcpp.14037', 'Siegel', 'Unconscious exposure as a treatment strategy for fear and anxiety: review of controlled experiments', 'J Child Psychol Psychiatry', 2025, '66', '98-121'),
 (31, '30287083', None, 'Carl', 'Virtual reality exposure therapy for anxiety and related disorders: A meta-analysis of randomized controlled trials', 'J Anxiety Disord', 2019, '61', '27-36'),
 (32, None, '10.1007/s10608-025-10667-1', 'Meckes', 'Testing judicious use of safety behaviors during exposure', 'Cogn Ther Res', 2025, '50', '341-359'),
 (34, None, '10.1007/s11222-016-9696-4', 'Vehtari', 'Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC', 'Stat Comput', 2017, '27', '1413-1432'),
 (35, None, '10.1177/1948550617697177', 'Lakens', 'Equivalence tests: a practical primer for t tests, correlations, and meta-analyses', 'Soc Psychol Personal Sci', 2017, '8', '355-362'),
 (37, '40210881', '10.1038/s41597-025-04908-x', 'Lor', 'SpiderPhy dataset: a multimodal dataset of physiological, psychometric and behavioral responses to fear stimuli', 'Sci Data', 2025, '12', '599'),
 (38, '39962218', '10.1038/s41597-025-04569-w', 'Zhang', 'SpiDa-MRI: behavioral and (f)MRI data of adults with fear of spiders', 'Sci Data', 2025, '12', '284'),
]
# refs 33, 36 = books (no PMID/DOI cited) -> UNRESOLVED by design; 39-43 = author companion docs -> N/A.

report = []
for (rid, pmid, doi, au, title, jr, yr, vol, pg) in REFS:
    row = {'ref': rid, 'issues': [], 'checked_via': []}
    # --- PubMed ---
    if pmid:
        try:
            d = get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json')
            res = d['result'].get(pmid, {})
            if res.get('error') or not res.get('title'):
                row['issues'].append(f'PMID {pmid}: not found in PubMed')
            else:
                row['checked_via'].append('pubmed')
                s = tsim(title, res.get('title',''))
                if s < 0.75:
                    row['issues'].append(f"title mismatch vs PubMed (sim={s:.2f}): PubMed='{res.get('title','')[:90]}'")
                a0 = (res.get('authors') or [{}])[0].get('name','')
                if norm(au).split()[0] not in norm(a0):
                    row['issues'].append(f"first author: cited '{au}' vs PubMed '{a0}'")
                pd_ = res.get('pubdate','') + ' ' + res.get('epubdate','')
                if str(yr) not in pd_ and str(yr) not in res.get('sortpubdate',''):
                    row['issues'].append(f"year: cited {yr} vs PubMed '{res.get('pubdate','')}'")
                sv = res.get('volume','')
                if vol and sv and norm(vol) != norm(sv):
                    row['issues'].append(f"volume: cited '{vol}' vs PubMed '{sv}'")
                sp = res.get('pages','')
                if pg and sp and norm(pg).replace(' ','') != norm(sp).replace(' ',''):
                    row['issues'].append(f"pages: cited '{pg}' vs PubMed '{sp}'")
                sj = res.get('source','')
                if jr and sj and tsim(jr, sj) < 0.55 and norm(jr) not in norm(res.get('fulljournalname','')):
                    row['issues'].append(f"journal: cited '{jr}' vs PubMed '{sj}' / '{res.get('fulljournalname','')}'")
                if doi:
                    ids = {i['idtype']: i['value'] for i in res.get('articleids', [])}
                    pdoi = ids.get('doi','')
                    if pdoi and norm(doi) != norm(pdoi):
                        row['issues'].append(f"DOI: cited '{doi}' vs PubMed '{pdoi}'")
        except Exception as e:
            row['issues'].append(f'PubMed UNRESOLVED: {type(e).__name__}')
        time.sleep(0.45)
    # --- CrossRef ---
    if doi:
        try:
            d = get(f'https://api.crossref.org/works/{urllib.parse.quote(doi)}')
            m = d['message']
            row['checked_via'].append('crossref')
            ct = (m.get('title') or [''])[0]
            s = tsim(title, ct)
            if s < 0.70:
                row['issues'].append(f"title mismatch vs CrossRef (sim={s:.2f}): CrossRef='{ct[:90]}'")
            fam = (m.get('author') or [{}])[0].get('family','')
            if fam and norm(au).split()[0] not in norm(fam) and norm(fam) not in norm(au):
                row['issues'].append(f"first author: cited '{au}' vs CrossRef '{fam}'")
            cyrs = []
            for k in ('published-print','published-online','issued'):
                dp = (m.get(k) or {}).get('date-parts', [[None]])
                if dp and dp[0] and dp[0][0]: cyrs.append(dp[0][0])
            if cyrs and yr not in cyrs and (yr+1) not in cyrs and (yr-1) not in cyrs:
                row['issues'].append(f"year: cited {yr} vs CrossRef {sorted(set(cyrs))}")
            cv = m.get('volume','')
            if vol and cv and norm(vol) != norm(cv):
                row['issues'].append(f"volume: cited '{vol}' vs CrossRef '{cv}'")
            cp = m.get('page','')
            if pg and cp and norm(pg).replace(' ','') != norm(cp).replace(' ',''):
                row['issues'].append(f"pages: cited '{pg}' vs CrossRef '{cp}'")
        except urllib.error.HTTPError as e:
            row['issues'].append(f"DOI '{doi}': CrossRef HTTP {e.code}" + (' -- DOI DOES NOT RESOLVE' if e.code==404 else ' (UNRESOLVED)'))
        except Exception as e:
            row['issues'].append(f'CrossRef UNRESOLVED: {type(e).__name__}')
        time.sleep(0.35)
    if not row['checked_via'] and not row['issues']:
        row['issues'].append('no PMID/DOI cited -- UNRESOLVED (needs manual check)')
    report.append(row)

ok = [r for r in report if not r['issues']]
bad = [r for r in report if r['issues']]
print(f"CHECKED {len(report)} entries: OK={len(ok)}  FLAGGED={len(bad)}")
print("OK refs:", [r['ref'] for r in ok])
print()
for r in bad:
    print(f"[ref {r['ref']}] via {','.join(r['checked_via']) or 'none'}:")
    for i in r['issues']:
        print('   -', i)
