
import string

def getDomainInt(n):
    if n < 1: return

    def getDomainNumber(domain, n):
        if len(domain) == n: yield domain
        else:            
            for a in string.ascii_lowercase + string.digits:
                for b in getDomainNumber(domain + a, n):
                    yield b    
    for a in getDomainNumber("", n): yield a

def getDomain(*args):
    sum = 0
    words = []
    nums = []
    results = list(args)
    for i, a in enumerate(args):
        if type(a) == int:
            sum += a
            nums.append((i, a))
        elif type(a) == str:
            words.append((i, a))
        else:
            pass
    domain = ""
      
    for a in getDomainInt(sum):
        begin = 0 
        for i, num in nums:
            results[i] = a[begin:begin + num]
            begin += num
        yield reduce(lambda a, b: a+b, results)

def matchDomain(meta_domain):
    result = []
    for element in meta_domain.split("*"):
        result.append(element)
        result.append(1)
    result.pop()
    result = filter(lambda a: a != "", result)
    for domain in getDomain(*result):
        yield domain

def getDomainByFile(domain_file):
    with open(domain_file) as f:
        for line in f.readlines():
            yield line.strip()

if __name__ == "__main__":

    #for domain in getDomain("fuck", 1, "baidu", 1, ".com"):
    #    print domain
    
    for domain in matchDomain("fuck**baidu*.org"):
        print domain

   