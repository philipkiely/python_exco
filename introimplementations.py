#For positive integer n, print every number 1 to n (inclusive) with fizzbuzz
def fizzbuzz(n):
    for i in range(1, (n + 1)):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 5 == 0:
            print("Buzz")
        elif i % 3 == 0:
            print("Fizz")
        else:
            print(i)

#Calculate n! recursively
def recfactorial(n):
    if n == 0:
        return 1
    else:
        return n * recfactorial(n-1)

#calculate n! using range
def pyfactorial(n):
    ret = 1
    for i in range(1, (n + 1)):
        ret *= i
    return ret

#Given a name ("First Last"), make a grinnell email
def grinnell_email(name):
    name = name.lower()
    name = name.split(" ")
    ret = ""
    ret += name[1] + name[0]
    ret = ret[0:8]
    ret += "@grinnell.edu"
    return ret

#demonstrate all functiions when file is run
if __name__ == "__main__":
    fizzbuzz(30)
    print("recfactorial(0) = {}".format(recfactorial(0)))
    print("recfactorial(1) = {}".format(recfactorial(1)))
    print("recfactorial(8) = {}".format(recfactorial(8)))
    print("pyfactorial(0) = {}".format(pyfactorial(0)))
    print("pyfactorial(1) = {}".format(pyfactorial(1)))
    print("pyfactorial(8) = {}".format(pyfactorial(8)))
    print(grinnell_email("Philip Kiely"))
    print(grinnell_email("Griffin Mareske"))
