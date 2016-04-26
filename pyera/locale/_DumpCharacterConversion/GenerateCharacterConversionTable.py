import msgpack

v = []
f = open("map_dumped.txt","r")
for l in f:
    v.append([int(i) for i in l.strip().split('\t')])
vv=[]
for o,n,w in v:
    newseg = False
    if len(vv) == 0:
        newseg = True
    else:
        (ob, oe), nn, ww = vv[-1]
        if not (o == oe and nn == n and ww == w):
            newseg = True
    if newseg:
        vv.append(((o, o + 1), n, w))
    else:
        vv[-1] = ((ob, o + 1), nn, ww)

for i in range(len(vv)):
    (ob, oe), nn, ww = vv[i]
    if ob + 1 == oe:
        vv[i] = (ob, nn, ww)

h2f, f2h = [],[]
for o,n,w in vv:
    if isinstance(o, tuple):
        h2f.append((o,w))
        f2h.append((o,n))
    else:
        if o != w:
            h2f.append((o,w))
        if o != n:
            f2h.append((o,n))

def retrieve(s, v):
    def binsearch(b, e):
        if e - b == 0:
            return -1
        m = (b + e) // 2
        mv, t = s[m]
        if isinstance(mv, tuple):
            mvb, mve = mv
            if v < mvb:
                return binsearch(b, m)
            elif v >= mve:
                return binsearch(m + 1, e)
            else:
                return t
        elif v < mv:
            return binsearch(b, m)
        elif v > mv:
            return binsearch(m + 1, e)
        else:
            return t
            
    return binsearch(0, len(s))

test = open("map_reconstructed.txt",'w')
for i in range(0x110000):
    if 0xD800 <= i < 0xE000:
        continue
    o,n,w = i, retrieve(f2h, i), retrieve(h2f, i)
    if n == -1:
        n = i
    if w == -1:
        w = i
    if o == n == w:
        continue
    test.write("%d\t%d\t%d\n" % (o,n,w))
test.close()

codegen = open("cctable.py",'w')
codegen.write("H2F_msgpack = ")
codegen.write(repr(msgpack.packb(h2f)))
codegen.write("\n")
codegen.write("F2H_msgpack = ")
codegen.write(repr(msgpack.packb(f2h)))
codegen.write("\n")
codegen.close()

