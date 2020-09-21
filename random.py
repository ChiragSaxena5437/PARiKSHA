import math
n=int(input())
p=float(input())
q=1-p
for i in range(n):
    temp1=q**(i)
    if(i<=n-2):
        print(round(p*temp1,4),end=" ")
print(round(temp1,4))
print(round(1/p,4))
temp=p**2
temp4=1-p
print(round(temp4/temp,4))
print('\n')