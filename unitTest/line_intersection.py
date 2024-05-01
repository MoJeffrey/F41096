def line_intersection(A1, A2, B1, B2, C1, C2):
    """
    返回两条线段(A1,A2)和(B1,B2)的交点，如果不存在则返回None
    """
    def ccw(A, B, C):
        """
        判断ABC是否逆时针排列
        """
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    def intersect(A, B):
        """
        判断线段AB和CD是否相交
        """
        return ccw(A[0], B[0], B[1]) != ccw(A[1], B[0], B[1]) and ccw(A[0], A[1], B[0]) != ccw(A[0], A[1], B[1])

    A = tuple(A1), tuple(A2)
    B = tuple(B1), tuple(B2)
    C = tuple(C1), tuple(C2)

    if intersect(A, C):
        return "C与线段A相交"
    elif intersect(B, C):
        return "C与线段B相交"
    else:
        return "C与线段A和B都不相交"

# 线段A、B、C的端点
A1 = (1, 1)
A2 = (4, 4)
B1 = (1, 4)
B2 = (4, 1)
C1 = (2, 2)
C2 = (3, 3)

# 判断线段C与线段A和B是否相交
result = line_intersection(A1, A2, B1, B2, C1, C2)
print(result)
