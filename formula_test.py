import telefunken_n3psi as t3
import telefunken_n2psi as t2
import telefunken_n1psi as t1


filepath = 'C:\\Users\\Maisha\\Dropbox\\MB_dev\\Telefunken\\testfiles\\testdata-10000-250.csv'

print("N3PSI")
t3.run_telefunken(filepath)
print("N2PSI")
t2.run_telefunken(filepath)
print("N1PSI")
t1.run_telefunken(filepath)