# Auto-generated. Do not edit.
from opendp.v1._convert import *
from opendp.v1._lib import *
from opendp.v1.mod import *
from opendp.v1.typing import *


def make_base_laplace(
    scale,
    D: RuntimeTypeDescriptor = "AllDomain<T>"
) -> Measurement:
    """Make a Measurement that adds noise from the laplace(`scale`) distribution to a scalar value.
    Adjust D to noise vector-valued data.
    
    
    `This constructor is supported by the linked proof. <https://www.overleaf.com/read/brvrprjhrhwb>`_
    
    :param scale: Noise scale parameter of the laplace distribution.
    :param D: Domain of the data type to be privatized. Valid values are VectorDomain<AllDomain<T>> or AllDomain<T>
    :type D: RuntimeTypeDescriptor
    :return: A base_laplace step.
    :rtype: Measurement
    :raises AssertionError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type-argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    # Standardize type arguments.
    D = RuntimeType.parse(type_name=D, generics=["T"])
    T = get_domain_atom_or_infer(D, scale)
    D = D.substitute(T=T)
    
    # Convert arguments to c types.
    scale = py_to_c(scale, c_type=ctypes.c_void_p, type_name=T)
    D = py_to_c(D, c_type=ctypes.c_char_p)
    
    # Call library function.
    function = lib.opendp_meas__make_base_laplace
    function.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    function.restype = FfiResult
    
    return c_to_py(unwrap(function(scale, D), Measurement))


def make_base_gaussian(
    scale,
    D: RuntimeTypeDescriptor = "AllDomain<T>"
) -> Measurement:
    """Make a Measurement that adds noise from the gaussian(`scale`) distribution to the input.
    Adjust D to noise vector-valued data.
    
    :param scale: noise scale parameter to the gaussian distribution
    :param D: Domain of the data type to be privatized. Valid values are VectorDomain<AllDomain<T>> or AllDomain<T>
    :type D: RuntimeTypeDescriptor
    :return: A base_gaussian step.
    :rtype: Measurement
    :raises AssertionError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type-argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    # Standardize type arguments.
    D = RuntimeType.parse(type_name=D, generics=["T"])
    T = get_domain_atom_or_infer(D, scale)
    D = D.substitute(T=T)
    
    # Convert arguments to c types.
    scale = py_to_c(scale, c_type=ctypes.c_void_p, type_name=T)
    D = py_to_c(D, c_type=ctypes.c_char_p)
    
    # Call library function.
    function = lib.opendp_meas__make_base_gaussian
    function.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    function.restype = FfiResult
    
    return c_to_py(unwrap(function(scale, D), Measurement))


def make_base_geometric(
    scale,
    bounds: Any = None,
    D: RuntimeTypeDescriptor = "AllDomain<i32>",
    QO: RuntimeTypeDescriptor = None
) -> Measurement:
    """Make a Measurement that adds noise from the geometric(`scale`) distribution to the input.
    Adjust D to noise vector-valued data.
    
    :param scale: noise scale parameter to the geometric distribution
    :param bounds: Set bounds on the count to make the algorithm run in constant-time.
    :type bounds: Any
    :param D: Domain of the data type to be privatized. Valid values are VectorDomain<AllDomain<T>> or AllDomain<T>
    :type D: RuntimeTypeDescriptor
    :param QO: Data type of the sensitivity, scale, and budget.
    :type QO: RuntimeTypeDescriptor
    :return: A base_geometric step.
    :rtype: Measurement
    :raises AssertionError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type-argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    # Standardize type arguments.
    D = RuntimeType.parse(type_name=D)
    QO = RuntimeType.parse_or_infer(type_name=QO, public_example=scale)
    T = get_domain_atom(D)
    OptionT = RuntimeType(origin='Option', args=[RuntimeType(origin='Tuple', args=[T, T])])
    
    # Convert arguments to c types.
    scale = py_to_c(scale, c_type=ctypes.c_void_p, type_name=QO)
    bounds = py_to_c(bounds, c_type=AnyObjectPtr, type_name=OptionT)
    D = py_to_c(D, c_type=ctypes.c_char_p)
    QO = py_to_c(QO, c_type=ctypes.c_char_p)
    
    # Call library function.
    function = lib.opendp_meas__make_base_geometric
    function.argtypes = [ctypes.c_void_p, AnyObjectPtr, ctypes.c_char_p, ctypes.c_char_p]
    function.restype = FfiResult
    
    return c_to_py(unwrap(function(scale, bounds, D, QO), Measurement))


def make_base_stability(
    n: int,
    scale,
    threshold,
    MI: SensitivityMetric,
    TIK: RuntimeTypeDescriptor,
    TIC: RuntimeTypeDescriptor = "i32"
) -> Measurement:
    """Make a Measurement that implements a stability-based filtering and noising.
    
    :param n: Number of records in the input vector.
    :type n: int
    :param scale: Noise scale parameter.
    :param threshold: Exclude counts that are less than this minimum value.
    :param MI: Input metric.
    :type MI: SensitivityMetric
    :param TIK: Data type of input key- must be hashable/categorical.
    :type TIK: RuntimeTypeDescriptor
    :param TIC: Data type of input count- must be integral.
    :type TIC: RuntimeTypeDescriptor
    :return: A base_stability step.
    :rtype: Measurement
    :raises AssertionError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type-argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    # Standardize type arguments.
    MI = RuntimeType.parse(type_name=MI)
    TIK = RuntimeType.parse(type_name=TIK)
    TIC = RuntimeType.parse(type_name=TIC)
    
    # Convert arguments to c types.
    n = py_to_c(n, c_type=ctypes.c_uint)
    scale = py_to_c(scale, c_type=ctypes.c_void_p, type_name=MI.args[0])
    threshold = py_to_c(threshold, c_type=ctypes.c_void_p, type_name=MI.args[0])
    MI = py_to_c(MI, c_type=ctypes.c_char_p)
    TIK = py_to_c(TIK, c_type=ctypes.c_char_p)
    TIC = py_to_c(TIC, c_type=ctypes.c_char_p)
    
    # Call library function.
    function = lib.opendp_meas__make_base_stability
    function.argtypes = [ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    function.restype = FfiResult
    
    return c_to_py(unwrap(function(n, scale, threshold, MI, TIK, TIC), Measurement))


def make_alp_histogram(
    n: int,
    scale,
    beta,
    K: RuntimeTypeDescriptor,
    alpha = 4.0,
    size_factor: int = 30,
    C: RuntimeTypeDescriptor = None,
    T: RuntimeTypeDescriptor = None
):
    """Make a Measurement that returns an approximate laplace projection queryable.
    
    :param n: Number of records in the input vector.
    :type n: int
    :param alpha: Parameter for trade-off between randomized response and scaling.
    :param scale: Noise scale parameter.
    :param beta: Parameter for clamping values. Upper bound of values to store.
    :param size_factor: Used to determine size of ALP bitvector.
    :type size_factor: int
    :param K: Type of input query.
    :type K: RuntimeTypeDescriptor
    :param C: Type to collect counts.
    :type C: RuntimeTypeDescriptor
    :param T: Type to represent budget.
    :type T: RuntimeTypeDescriptor
    :return: A alp_histogram step.
    :raises AssertionError: if an argument's type differs from the expected type
    :raises UnknownTypeError: if a type-argument fails to parse
    :raises OpenDPException: packaged error from the core OpenDP library
    """
    # Standardize type arguments.
    K = RuntimeType.parse(type_name=K)
    C = RuntimeType.parse_or_infer(type_name=C, public_example=beta)
    T = RuntimeType.parse_or_infer(type_name=T, public_example=alpha)
    
    # Convert arguments to c types.
    n = py_to_c(n, c_type=ctypes.c_uint)
    alpha = py_to_c(alpha, c_type=ctypes.c_void_p, type_name=T)
    scale = py_to_c(scale, c_type=ctypes.c_void_p, type_name=T)
    beta = py_to_c(beta, c_type=ctypes.c_void_p, type_name=C)
    size_factor = py_to_c(size_factor, c_type=ctypes.c_uint32)
    K = py_to_c(K, c_type=ctypes.c_char_p)
    C = py_to_c(C, c_type=ctypes.c_char_p)
    T = py_to_c(T, c_type=ctypes.c_char_p)
    
    # Call library function.
    function = lib.opendp_meas__make_alp_histogram
    function.argtypes = [ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    function.restype = FfiResult
    
    return c_to_py(unwrap(function(n, alpha, scale, beta, size_factor, K, C, T), Measurement))
