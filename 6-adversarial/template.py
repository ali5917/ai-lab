'''

Minimax Steps

Base case — if leaf or depth 0, return the node's value
Maximizer — start at -inf, take max over children (flip to minimizer)
Minimizer — start at +inf, take min over children (flip to maximizer)
Store result in node.minmaxValue, return it up

Alpha-Beta Steps

Base case — if leaf or depth 0, return the node's value
Maximizer — start at -inf, take max over children (flip to minimizer)
Minimizer — start at +inf, take min over children (flip to maximizer)
Store result in node.minmaxValue, return it up
Pass alpha and beta down every call (alpha=-inf, beta=+inf at root)
After each child:
    Maximizer: alpha = max(alpha, value) → prune if alpha >= beta
    Minimizer: beta = min(beta, value) → prune if alpha >= beta

----------------------------------------------------------
- Alpha = Best for Maximizer. Beta = Best for Minimizer  |
----------------------------------------------------------

'''