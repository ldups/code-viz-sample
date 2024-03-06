import numpy as np
import matplotlib.pyplot as plt
import scipy as scp

def get_straight_line_val( x_val,m=-0.5, b=4):
    return x_val*m + b

def get_parabola_val(x_val,m1=-0.29, m0=-1, b=12.5):
    return (x_val**2)*m1 + x_val*m0 + b

def get_comp_func_val(x_val):
    term1 = x_val+1.0
    term2 = -1 * x_val**2.0
    return 1 + (10.0*(term1) * np.exp(term2))

def get_percent_diff(observed, true):
    return abs((true-observed)/true)*100

if __name__ == '__main__':
    width_list = np.array([2,1,0.5,0.25,0.01])
    func1_areas = []
    func2_areas = []
    func3_areas = []

    func1_true = 40
    func2_true = 100.83
    func3_true = 27.72

    for width in width_list:
        func1_area = 0
        func2_area = 0
        func3_area = 0
        for i in np.arange(-5,5+width,width):
            mid_point = i + width / 2
            func1_val = get_straight_line_val(mid_point,-0.5, 4)
            func1_area += func1_val * width
            func2_val = get_parabola_val(mid_point,-0.29, -1, 12.5)
            func2_area += func2_val * width
            func3_val = get_comp_func_val(mid_point)
            func3_area += func3_val * width

        func1_areas.append(func1_area)
        func2_areas.append(func2_area)
        func3_areas.append(func3_area)
    
    func1_diffs = []
    func2_diffs = []
    func3_diffs = []

    func1_diffs = np.array([get_percent_diff(func1_true,area) for area in func1_areas])
    func2_diffs = np.array([get_percent_diff(func2_true,area) for area in func2_areas])
    func3_diffs = np.array([get_percent_diff(func3_true,area) for area in func3_areas])

    plt.plot(width_list, func1_diffs, label='linear function')
    plt.plot(width_list, func2_diffs, label='parabolic function')
    plt.plot(width_list, func3_diffs, label='exponential function')
    plt.xlabel('rectangle width size')
    plt.ylabel('percent difference between true and calculated areas')
    plt.gca().invert_xaxis()
    plt.legend()
    plt.title('Area Under Curve Estimated With Rectangles vs. True Value')
    plt.show()

    f = lambda x: get_straight_line_val(x)
    print(f'function 1 true area: {func1_true}, function 1 area calculated by scipy: {scp.integrate.quadrature(f,-5,5)[0]}, best estimation of function 1 with rectangles: {func1_areas[-1]}')
    f = lambda x: get_parabola_val(x)
    print(f'function 2 true area: {func2_true}, function 2 area calculated by scipy: {scp.integrate.quadrature(f,-5,5)[0]}, best estimation of function 2 with rectangles: {func2_areas[-1]}')
    f = lambda x: get_comp_func_val(x)
    print(f'function 3 true area: {func3_true}, function 3 area calculated by scipy: {scp.integrate.quadrature(f,-5,5)[0]}, best estimation of function 3 with rectangles: {func3_areas[-1]}')
