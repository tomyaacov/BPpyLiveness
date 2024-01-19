from dwyer_patterns.utils import *
from bppy.model.b_thread import b_thread
from bppy.model.sync_statement import waitFor, request, block, mustFinish

# patterns from https://smlab.cs.tau.ac.il/syntech/patterns/MR15patterns.pdf
# https://spot.lre.epita.fr/app/


@b_thread
def pat_0():
    """
    F ( G p)
    """
    while True:
        e = yield {waitFor: true(), mustFinish: True}
        if e in non_det:
            break
    yield {block: Not(p)}

@b_thread
def pat_8():  # done
    """
    Kind: Existence: p becomes true
    Scope: After q
    LTL:
        G !q || F (q && F p)
    """
    yield {waitFor: And(q, Not(p))}
    yield {waitFor: p, mustFinish: True}


@b_thread
def pat_10():  # done
    """
    Kind: Existence: p becomes true
    Scope: After q until r
    LTL:
        G (!(q && !r) || (!r U (p && !r)))
    """
    while True:
        yield {waitFor: And(Not(p), q, Not(r))}
        yield {waitFor: p, block: r, mustFinish: True}


@b_thread
def pat_23():
    """
    Kind: Precedence: s precedes p
    Scope: After q
    LTL:
        G !q || F (q && (s V (!p || s)))

        G !q || F(q & (!p W s))
    """
    e = yield {waitFor: q}
    if e in Not(s):
        yield {waitFor: s, block: And(p, Not(s))}




    e = yield {waitFor: Or(Not(q),
                       And(Not(p), q, Not(s)),
                       Or(Not(q), Not(s)),
                       And(q, s)), mustFinish: True}
    # if e in Not(q):
    #     if non_deterministic(e):
    #         # 2
    #     else:
    #         # 4
    # elif e in Not(s):
    #     if e in p:
    #         # 4
    #     else:
    #         if non_deterministic(e):
    #             # 3
    #         else:
    #             # 4
    # else:
    #     # 1



    yield {waitFor: And(q, s) }
    while True:
        e = yield {waitFor: Or(And(q, s), And(Not(p), q, Not(s))), mustFinish: True}
        if e in And(q,s):
            break
        if e in And(Not(p),q,Not(s)):
            if non_deterministic(e):
                continue
            yield {waitFor: s, block: And(p, Not(s))}
            break


@b_thread
def complement_pat_23():
    """
    Kind: Precedence: s precedes p
    Scope: After q
    LTL:
        G !q || F (q && (s V (!p || s)))
    """
    yield {waitFor: q, mustFinish: True}
    while True:
        e = yield {waitFor: Or(And(q, s), And(Not(p), q, Not(s)))}
        if e in And(q,s):
            break
        if e in And(Not(p),q,Not(s)):
            if non_deterministic(e):
                continue
            e = yield {waitFor: Or(s, And(p, Not(s))), mustFinish: True}
            if e in And(p, Not(s)):
                yield {waitFor: false}
            break
    yield {waitFor: false, mustFinish: True}

@b_thread
def pat_26():  # done
    """
    Kind: Response: s responds to p
    Scope: Globally
    LTL:
        G (!p || F s)
    """
    while True:
        yield {waitFor: And(p, Not(s))}
        yield {waitFor: s, mustFinish: True}


@b_thread
def pat_28():  # done
    """
    Kind: Response: s responds to p
    Scope: After q
    LTL:
        G (!q || G (!p || F s))
    """
    e = yield {waitFor: q}
    if (not e.p) or e.s:
        yield {waitFor: And(p, Not(s))}
    while True:
        yield {waitFor: s, mustFinish: True}
        yield {waitFor: And(p, Not(s))}


@b_thread
def pat_30():  # done
    """
    Kind: Response: s responds to p
    Scope: After q until r
    LTL:
        G (!(q && !r) || (r V (!p || r || (!r U (!r && s)))))
    """
    while True:
        e = yield {waitFor: And(q, Not(r))}
        if (not e.p) or e.s:
            e = yield {waitFor: Or(r, And(p, Not(s)))}
        while not e.r:
            yield {waitFor: s, block: r, mustFinish: True}
            e = yield {waitFor: Or(r, And(p, Not(s)))}

@b_thread
def pat_41():
    """
    Kind: Response Chain: p responds to s,t
    Scope: Globally
    LTL:
       G (XF (t && F p) || !(s && XF t))
    """
    while True:
        yield {waitFor: s}
        yield {waitFor: t}
        yield {waitFor: p, mustFinish: True}

    # TODO: this is not correct




@b_thread
def pat_42():
    """
    Kind: Response Chain: p responds to s,t
    Scope: Before r
    LTL:
       ((X(!r U (t && F p)) || !(s && X(!r U t))) U r) || !F r
    """
    pass


@b_thread
def pat_43():
    """
    Kind: Response Chain: p responds to s,t
    Scope: After q
    LTL:
       G (!q || G (X(!t U (t && F p)) || !(s && XF t)))
    """
    pass


@b_thread
def pat_44():
    """
    Kind: Response Chain: p responds to s,t
    Scope: Between q and r
    LTL:
       G (((X(!r U (t && F p)) || !(s && X(!r U t))) U r) || !(q && F r))
    """
    pass


@b_thread
def pat_45():
    """
    Kind: Response Chain: p responds to s,t
    Scope: After q until r
    LTL:
       G (!q || ((X(!r U (t && F p)) || !(s && X(!r U t))) U (r || G (X(!r U (t && F p)) || !(s && X(!r U t))))))
    """
    pass


@b_thread
def pat_46():
    """
    Kind: Response Chain: s,t responds to p
    Scope: Globally
    LTL:
       G (!p || F (s && XF t))
    """
    while True:
        yield {waitFor: p}
        while True:
            e = yield {waitFor: true(), mustFinish: True}
            if e in non_det:
                break
        yield {block: Not(s), waitFor: true(), mustFinish: True}
        yield {block: Not(t), waitFor: true(), mustFinish: True}


@b_thread
def pat_48():
    """
    Kind: Response Chain: s,t responds to p
    Scope: After q
    LTL:
       G (!q || G (!p || (s && XF t)))
    """
    while True:
        e = yield {waitFor: q}
        if not e.p:
            e = yield {waitFor: p}
        while True:
            yield {waitFor: s, mustFinish: True}
            while True:
                e = yield {waitFor: true(), block: Not(t), mustFinish: True}
                if not e.s:
                    break



@b_thread
def pat_50():
    """
    Kind: Response Chain: s,t responds to p
    Scope: After q until r
    LTL:
       G (!q || ((!p || (!r U (!r && s && X(!r U t)))) U (r || G (!p || (s && XF t)))))
    """
    pass


@b_thread
def pat_51():
    """
    Kind: Constrained Chain: s,t without z responds to p
    Scope: Globally
    LTL:
       G (!p || F (s && !z && X(!z U t)))
    """
    pass


@b_thread
def pat_53():
    """
    Kind: Constrained Chain: s,t without z responds to p
    Scope: After q
    LTL:
       G (!q || G (!p || (s && !z && X(!z U t))))
    """
    pass


@b_thread
def pat_55():
    """
    Kind: Constrained Chain: s,t without z responds to p
    Scope: After q until r
    LTL:
       G (!q || ((!p || (!r U (!r && s && !z && X((!r && !z) U t)))) U (r || G (!p || (s && !z && X(!z U t))))))
    """
    pass
