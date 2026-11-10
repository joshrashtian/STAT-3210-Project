# STAT-3210-Project
Code for Stats Project in STAT3210 Cal Poly, which mesasures various language speeds to see which is worth the performance to development time.

# How It Works
I measured all of the following languages with the following flow, copied to match each language:

```
parse count
   start timer
   repeat count times:
       open the file
       make a scanner for it
       scan every line, adding to total
       close the file
   stop timer
```

With that flow in mind, some languages have more libraries than others, or need more imports. Due to that and us measuring raw time, we used a timer in each langauge. Go took 2 lines to solve this, while C required a helper function.
