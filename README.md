# Leontieff-Model-Reproducible-Result
The link to the data: [Click here to download](http://stats.oecd.org/wbos/fileview2.aspx?IDFile=59a3d7f2-3f23-40d5-95ca-48da84c0f861)
Or go to the website [OECD Inter-Country Input-Output (ICIO) Tables](https://www.oecd.org/sti/ind/inter-country-input-output-tables.htm)

**Context:**

Economic data is often highly asymmetric. As a result, computational economics often has to place a focus on the tails of distributions rather than on the body.
We will focus on the occurence of large and rare effects. Such effects can, for example, be measured as the expected size of the largest plausible shocks, say the 99% quantile, or the “upper 1% quantile”.
(The 99% quantile here would be a shock such that for 99% of sectors, the shock is smaller and only for 1% the shock is larger). The estimates for tail values may be volatile.

**Task:**

1. Whether the upper 1% quantile in the demand shock as computed by script is reproducible.
2. What measures could be taken to make it reproducible, if that is not the case?
3. Produce a reproducible result for the upper 1% quantile of the resulting effect of demand shocks by 0.3 (30%), 0.7 (70%) and 1.0 (100%) to individual
   random sectors in random countries on the world economy.

**Output:**

<img src="https://github.com/MohidulHaqueTushar/Leontieff-Model-Reproducible-Result/blob/main/Effect%20of%20different%20shock_sizes%20on%20upper%201%25%20quantile.png" alt="result" width="500"/>
