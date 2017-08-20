Arcade Pig
Created by Leo Tindall

This is an implementation in Rust of a classic dice game called Pig.
Pig is essentially a game of probabilisitc edge-walking; the player
is given the choice, over and over, of either keeping their current
score or risking it all for a higher score.

The source code's 124 lines include a pseudo-random number generator
implementation, because the Rust standard library doesn't include one.
