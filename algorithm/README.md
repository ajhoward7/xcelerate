# Notes

All of our training plans will be created from a set of pre-defined run-vectors which specify distances to be run and workout types on particular days. Our algorithm will look to focus on the correct part of this "vector" according to user preferences and history, scaling the run distances as appropriate.

A full training plan will be created when the plan is initialised and this will be modified at the end of each week once training has been submitted for the previous week.
 
**Construction of training plan:**
1. Runners will be placed into category Novice/Intermediate(/Advanced) at their discretion.
2. The number of days to run in each week will be decided based on their preferences and running history, placing us at a unique point in the vector of "runs until race"
3. Each individual workout will be scaled such that the total weekly mileage is "appropriate"

**Dynamically adjusting training plans:**
- The number of miles per week and days run per week will be adjusted based on these statistics for the last 2-3 weeks (a weighted average with the initial planned miles)  
- The runner will have a checkbox to provide feedback on how their week has gone (too hard / about right / too easy), which will further adjust their tranining by factor of 20%  

**Deciding weekly mileage levels:**
- NOVICE: Peak mileage levels for each distance will be pre-defined by us, each plan will start at 50% of this and increase the level by 10% every 2nd week
- INTERMEDIATE -- looking to keep training steady: mileage will remain approximately constant with a 5 mile reduction every 3rd week
- INTERMEDIATE -- looking to increase training: mileage will start at previous levels and increase by 10% every 2nd week until increased by 50%

**Information we need to perform this algorithm (i.e. preferences / information provided):**

NOVICE:
- Number of days willing to run per week
- Approximate past training levels if applicable (DO WE WANT ANY INFORMATION ABOUT PAST TRAINING FOR NOVICE OR SHOULD WE PUT ALL ON THE SAME BASELINE?)

INTERMEDIATE:
- Average number of days run per week beforehand
- Approximate previous mileage (miles/run) beforehand
- Are they looking to keep training levels from before or increase? (If increase, how many days a week do you want to run?)

