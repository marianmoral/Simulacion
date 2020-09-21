import numpy as np
from scipy.integrate import ode
from scipy.optimize import curve_fit
from lmfit import minimize, Parameters
import json
from tqdm import tqdm
from bfmplot import pl
from bfmplot import brewer_qualitative, simple_cycler, markers

import bfmplot as bp

#brewer_qualitative[6] = brewer_qualitative[1]

colors = simple_cycler(brewer_qualitative)

class REPL(dict):

    def __init__(self, items):
        self.items = items

    def __getitem__(self,i):
        try:
            return self.items[i]
        except KeyError as e:
            return i



with open('../data/all_confirmed_cases_with_population.json','r') as f:
    data = json.load(f)

tuplelist = [ (p, d)  for p, d in data.items()\
                               if max(d['cases']) >= 20\
                               and len(np.where(np.logical_and(np.array(d['times'])<=12,
                                                               np.array(d['cases'])>0))[0])\
                                   >= 8
                             ]

colors

tuplelist = sorted([ t for t in tuplelist ],key=lambda x: -max(x[1]['cases']))

n_fits = len(tuplelist)
n_col = int(np.ceil(np.sqrt(n_fits)))
n_row = 2
n_col = 4
fig, ax = pl.subplots(n_row,n_col,figsize=(8,3))
ax = ax.flatten()

titlemap = REPL({'mainland_china':'All w/o Hubei'})

letter = "abcdefg"
roman = [ "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix"]

i = -1
for province, pdata in tqdm(tuplelist[2:10]):
    i += 1
    print(province)

    t = np.array(pdata['times'])
    cases = np.array(pdata['cases'])
    if pdata['dates'][0] == "2020-01-22 12:00:00":
        t += 14/24
    else:
        dt = 0

    if max(cases) <= 20:
        continue


    i0 = np.where(cases>0)[0][0]
    t = t[i0:]
    cases = cases[i0:]

    i1 = np.where(t<=12)[0][-1]
    _t = t[:i1+1]
    _cases = cases[:i1+1]
    print(t, cases)

    if len(t) < 8:
        continue

    f = lambda x, mu, B: B*(x)**mu
    p,_ = curve_fit(f, _t, _cases, [1.5,4.5])

    print(p)

    tt = np.logspace(np.log(t[0]), np.log(t[-1]), base=np.exp(1))

    pl.sca(ax[i])

    ax[i].text(0.7,0.2,
            "$\mu={0:4.2f}$".format(p[0]),
            transform=ax[i].transAxes,
            ha='right',
            va='bottom',
            bbox={'facecolor':'w','edgecolor':'w','pad':0},
            zorder = -1000,
            )
    ax[i].text(0.7,0.03,
            titlemap[province],
            transform=ax[i].transAxes,
            ha='right',
            va='bottom',
            bbox={'facecolor':'w','edgecolor':'w','pad':0}
            )
    pl.plot(t, cases,marker=markers[i+2],c=colors[i+2],label='data',mfc='None')
    pl.plot(tt, f(tt,*p),c='k',lw=1,label='$Q_I$')

    _c = i % (n_col)
    _r = i // (n_col)
    if _r == n_row-1:
        pl.xlabel('days since Jan. 20th')
    if _c == 0 and _r == 0:
        pl.ylabel('confirmed cases',)
        pl.gca().yaxis.set_label_coords(-0.3,-0.2)
    pl.xlim([1,30])
    pl.xscale('log')
    pl.yscale('log')

    ylim = ax[i].set_ylim([1,2e3])
    ylim = ax[i].get_ylim()
    ax[i].plot([12,12],ylim,':')

    ax[i].text(0.03,0.97,
            "{}".format(roman[i]),
            transform=ax[i].transAxes,
            ha='left',
            va='top',
            fontweight='bold',
            fontsize=10,
            bbox={'facecolor':'w','edgecolor':'w','pad':0}
            )
    if i == 0:
        ax[i].text(0.75,0.45,
                "Feb. 2nd".format(p[0]),
                transform=ax[i].transAxes,
                ha='center',
                va='bottom',
                fontsize=9,
                bbox={'facecolor':'w','edgecolor':'w','pad':0}
                )
    if _r < n_row-1:
        [ x.set_visible(False) for x in ax[i].xaxis.get_major_ticks() ]
    ax[i].set_yticks([1,10,100,1000])

    bp.strip_axis(pl.gca())

ax[0].text(-0.4,1.1,
           'C',
            transform=ax[0].transAxes,
            ha='left',
            va='top',
            fontweight='bold',
            fontsize=14,
            bbox={'facecolor':'w','edgecolor':'w','pad':0}
        )

    
pl.gcf().tight_layout()
pl.gcf().subplots_adjust(wspace=0.3,hspace=0.3)
pl.gcf().savefig("powerlaw_fit_figures/fit_powerlaw_500.png",dpi=300)



pl.show()
