def 快排(left,right,array):
    if left>=right:
        return
    i,mid,j=left+1,left,right
    while i<j:
        while array[mid]>=array[i] and i<j:
            i+=1
        while array[mid]<=array[j] and i<j:
            j-=1
        #交换
        temp=array[i]
        array[i]=array[j]
        array[j]=temp
    #判断中间数的位置
    if array[mid] >= array[i]:
        #交换中间数
        temp = array[i]
        array[i] = array[mid]
        array[mid] = temp
        mid=i
    else:
        # 交换中间数
        temp = array[i-1]
        array[i-1] = array[mid]
        array[mid] = temp
        mid=i-1
    快排(left,mid-1,array)
    快排(mid+1,right,array)

def kp(array):
    if len(array)<2: return array
    else:
        min = [x for x in array[1:] if x < array[0]]
        mid = [z for z in array if z == array[0]]
        max = [d for d in array[1:] if d > array[0]]
        return kp(min)+mid+kp(max)

a=[1,5,3,10,6,8,7,5,11,8,9,2,8,7]
#快排(0,len(a)-1,a)
a=kp(a)
print(a)