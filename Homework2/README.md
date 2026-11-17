We can add a third algorithm called UCB1. Imagine you are a rapper launching a new song and using a small budget to run YouTube ads. You create four different ten-second video teasers to see which one brings in the most streams. Testing these manually wastes money on bad clips, and the other methods still have room for improvement.

While epsilon-greedy relies on random guesses and thompson sampling uses probabilities, UCB1 acts like an optimistic explorer. It looks at both the average success of a clip and how sure we are about those results. If a teaser clip has only been tested a few times, UCB1 gives it a helpful boost just in case it is actually the best choice.

To add this to our code, we can create a new UCB1 class and include its results in our comparison charts. 
