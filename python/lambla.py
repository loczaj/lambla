# Expanding limits of the stack (Linux only)
import sys, resource
sys.setrecursionlimit(40000)
resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))

# Church numbers
zero = lambda s: lambda z: z

succ = lambda num: lambda s: lambda z: s(num(s)(z))
one = succ(zero)
two = succ(one)

plus = lambda a, b: lambda s: lambda z: a(s)(b(s)(z))
four = plus(two, two)
five = plus(four, one)

write_int = lambda num: str(num(lambda x: x + 1)(0))
print(write_int(five), " = ", write_int(plus(two, plus(one, two))))

# Church boolean
true = lambda t: lambda f: t
false = lambda t: lambda f: f
zerop = lambda num: num(lambda x: false)(true)
_if = lambda cond: lambda trueBody: lambda falseBody: cond(trueBody)(falseBody) ()
print(_if(zerop(zero))(lambda: 'number is zero')(lambda: 'number is NON zero'))

# Predecessor: λn.λf.λx.n (λg.λh.h (g f)) (λu.x) (λu.u)
pred = lambda num: lambda s: lambda z: num(lambda g: lambda h: h(g(s))) (lambda u: z) (lambda u: u)
print('pred 2 = ' + write_int(pred(two)))

minus = lambda a, b: b (pred) (a)
three = minus(four, one)
print('4 - 1 = ' + write_int(three))

leqp = lambda a, b: zerop(minus(a, b))
lessp = lambda a, b: leqp(succ(a), b)
geqp = lambda a, b: zerop(minus(b, a))
greaterp = lambda a, b: geqp(a, succ(b))
write_bool = lambda a: str(a(True)(False))
print('3 <= 4 ' + write_bool(leqp(three, four)))
print('4 <= 3 ' + write_bool(leqp(four, three)))
print('2 >= 2 ' + write_bool(geqp(two, two)))
print('2 > 2 ' + write_bool(greaterp(two, two)))

_or = lambda a, b: lambda t: lambda f: b(t)(a(t)(f))
_and = lambda a, b: lambda t: lambda f: b(a(t)(f))(f)
_not = lambda a: lambda t: lambda f: a(f)(t)

equalp = lambda a, b: _and(leqp(a, b), leqp(b, a))
print('2 == 2 ' + write_bool(equalp(two, two)))
print('2 == 3 ' + write_bool(equalp(two, three)))

mult = lambda a, b: lambda s: lambda z: a(b(s)) (z)
ten = mult(five, two)
twelve = mult(three, four)
print('twelve = ' + write_int(twelve))

# Y-combinator
Y = lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))
fact = lambda f: lambda n: _if(leqp(n, one))(lambda: one)(lambda: mult(f(pred(n)), n))
print('fact 5 = ' + write_int(Y(fact)(five)))

# Prime numbers

div = lambda a, b: Y(lambda f: lambda m: _if(geqp(m, b))(lambda: plus(f(minus(m, b)), one))(lambda: zero))(a)
print('12 / 4 = ' + write_int(div(twelve, four)))

mod = lambda a, b: Y(lambda f: lambda x: _if(geqp(x, b))(lambda: f(minus(x, b)))(lambda: x))(a)
eleven = minus(twelve, one)
print('12 mod 5 = ' + write_int(mod(twelve, five)))
print('12 mod 4 = ' + write_int(mod(twelve, four)))
print('11 mod 4 = ' + write_int(mod(eleven, four)))

primep = lambda n: Y(lambda f: lambda d: _if(leqp(d, one))
    (lambda: true)(lambda: _if(zerop(mod(n, d)))(lambda: false)(lambda: f(pred(d)))))(div(n, two))
print('12 is prime: ' + write_bool(primep(twelve)))
print('11 is prime: ' + write_bool(primep(eleven)))
print('10 is prime: ' + write_bool(primep(ten)))
print('5 is prime: ' + write_bool(primep(five)))
print('4 is prime: ' + write_bool(primep(four)))
print('3 is prime: ' + write_bool(primep(three)))
print('2 is prime: ' + write_bool(primep(two)))

next_prime = lambda n: Y(lambda f: lambda i: _if(primep(i))(lambda: i)(lambda: f(succ(i))))(succ(n))
nth_prime = lambda n: Y(lambda f: lambda i: lambda p: _if(zerop(i))(lambda: p)(lambda: f(pred(i))(next_prime(p))))(n)(one)
print('10.th prime is: {0}'.format(write_int(nth_prime(ten))))

# List

cons = lambda h, t: lambda cnd: _if(cnd)(lambda: h)(lambda: t)
head = lambda cns: cns(true)
tail = lambda cns: cns(false)
c12 = cons(one, two)
print('Head is: {0}'.format(write_int(head(c12))))
print('Tail is: {0}'.format(write_int(tail(c12))))

list = lambda: cons(zero, zero)
put = lambda l, v: cons(succ(head(l)), cons(v, tail(l)))
at = lambda l, p: Y(lambda f: lambda _l: lambda i: _if(zerop(i))(lambda: head(_l))(lambda: f(tail(_l))(pred(i))))(l)(p)
size = lambda l: at(l, zero)
get = lambda l, p: at(l, minus(size(l), pred(p)))
l0 = list()
l1 = put(l0, one)
l2 = put(l1, two)
l3 = put(l2, three)
l4 = put(l3, five)
print('List size = ' + write_int(size(l4)))
print('List @ 1 = ' + write_int(get(l4, one)))
print('List @ 2 = ' + write_int(get(l4, two)))
print('List @ 3 = ' + write_int(get(l4, three)))
print('List @ 4 = ' + write_int(get(l4, four)))

write_int_list = lambda l: Y(
    lambda f: lambda p: _if(zerop(p))(lambda: '[ ')(lambda: f(pred(p)) + write_int(get(l, p)) + ' '))(size(l)) + ']'
print(write_int_list(l4))

sequence = lambda n: Y(lambda f: lambda p: _if(zerop(p))(lambda: list())(lambda: put(f(pred(p)), p))) (n)
print('Sequence of numbers up to 10: ' + write_int_list(sequence(ten)))

reverse = lambda l: Y(
    lambda f: lambda p: _if(zerop(p))(lambda: list())(lambda: put(f(pred(p)), at(l, p))))(size(l))
print('Reversed List = ' + write_int_list(reverse(l4)))

set = lambda l, p, v: Y(lambda f: lambda i: _if(zerop(i))(lambda: list())
    (lambda: put(f(pred(i)), _if(equalp(i, p))(lambda: v)(lambda: get(l, i)))))(size(l))
incr_at = lambda l, p: set(l, p, succ(get(l, p)))
incr_last = lambda l: incr_at(l, size(l))
print('Modified List = ' + write_int_list(incr_last(incr_at(set(l4, three, ten), two))))

swap = lambda l, p1, p2: set(set(l, p1, get(l, p2)), p2, (get(l, p1)))
print('Swapped List = ' + write_int_list(swap(l4, two, three)))

first_n_prime = lambda n: reverse(
    Y(lambda f: lambda i: lambda p: _if(zerop(i))(lambda: list())(lambda: put(f(pred(i))(next_prime(p)), p)))(n)(two))
print('First 10 prime numbers = ' + write_int_list(first_n_prime(ten)))

# Map, filter, reduce

map = lambda l, f: Y(lambda g: lambda p: _if(zerop(p))(lambda: list())
    (lambda: put(g(pred(p)), f(get(l, p))))) (size(l))

filter = lambda l, f: Y(lambda g: lambda p: _if(zerop(p))(lambda: list())
    (lambda: _if(f(get(l, p)))(lambda: put(g(pred(p)), get(l, p)))(lambda: g(pred(p))))) (size(l))

reduce = lambda l, f, i: Y(lambda g: lambda p: _if(zerop(p))(lambda: i)
    (lambda: f(g(pred(p)), get(l, p)))) (size(l))

li = sequence(five)
primes = map(li, nth_prime)
print('First 5 prime numbers: ' + write_int_list(primes))
print('Their product: ' + write_int(reduce(primes, mult, one)))

evens = filter(li, lambda n: zerop(mod(n, two)))
print('Even numbers below 5: ' + write_int_list(evens))

# N queens puzzle

distance = lambda a, b: _if(geqp(a, b))(lambda: minus(a, b))(lambda: minus(b, a))
# print(write_int(distance(ten, one)))
# print(write_int(distance(one, five)))
# print(write_int(distance(two, two)))

in_check_p = lambda r1, r2, c1, c2: _or((equalp(c1, c2)), equalp(distance(r1, r2), distance(c1, c2)))
print(write_bool(in_check_p(two, one, five, one)))

placement_valid_p = lambda pl, row: (lambda col:
    Y(lambda f: lambda r: _if(zerop(r))(lambda: true)
        (lambda: _and(_not(in_check_p(row, r, col, get(pl, r))), f(pred(r)))))(pred(row)))(get(pl, row))
# pl = list()
# pl = put(pl, three)
# pl = put(pl, five)
# pl = put(pl, ten)
# print(write_bool(placement_valid_p(pl, three)))

next_valid_placement = lambda pl: Y(
    lambda f: lambda pl: lambda row: _if(greaterp(row, size(pl)))(lambda: pl)
        (lambda: _if(greaterp(get(pl, row), size(pl)))
            (lambda: _if(equalp(row, one))(lambda: list())
                (lambda: f(incr_at(set(pl, row, one), pred(row)))(pred(row))))
            (lambda: _if(placement_valid_p(pl, row))(lambda: f(pl)(succ(row)))
                (lambda: f(incr_at(pl, row))(row))))) (pl)(two)


def print_solution(placement):
    vpl = next_valid_placement(placement)
    print("A solution of the " + write_int(size(placement)) + " queens puzzle: " + write_int_list(vpl))

pl = list()
pl = put(pl, one); print_solution(pl)
pl = put(pl, one); print_solution(pl)
pl = put(pl, one); print_solution(pl)
pl = put(pl, one); print_solution(pl)
pl = put(pl, one); print_solution(pl)
pl = put(pl, one); print_solution(pl)

print("All (4) solutions of the 6 queens puzzle:")
pl = next_valid_placement(incr_last(pl)); print(write_int_list(pl))
pl = next_valid_placement(incr_last(pl)); print(write_int_list(pl))
pl = next_valid_placement(incr_last(pl)); print(write_int_list(pl))
pl = next_valid_placement(incr_last(pl)); print(write_int_list(pl))
print(write_int_list(next_valid_placement(incr_last(pl))))

pl = put(pl, one); print_solution(pl)
pl = put(pl, one); print_solution(pl)
