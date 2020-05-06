import trik
A = trik.constant([[1, 2], [1, 3]], name='A')
x = trik.V([[1, 0,1],[1,0,1]], name='x')
x1 =trik.V([[1, 0],[1,1],[1,0]], name='x1')
b = trik.constant([3, 4], name='b')
#~ loss = pd.reduce_sum(((A @ x@(1**x1) + b)) ** 2) / 2
loss=A(trik.MM(),x)(trik.MM(),trik.constant(1)(trik.Pow(),x1))(trik.Plus(),b)(trik.Pow(),2)(trik.ReduceSum())(trik.Div(),2)
 
print('loss formula =\n{}\n'.format(loss))
print('loss =\n{}\n'.format(loss.val()))
  
x_gradient = loss.bprop(x)
print('x grad formula =\n{}\n'.format(x_gradient))
print('x grad =\n{}\n'.format(x_gradient.val()))