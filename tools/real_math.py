REAL_BITS = 128
REAL_FBITS = 40
REAL_IBITS = REAL_BITS - REAL_FBITS
REAL_ONE = 1 << REAL_FBITS
REAL_HALF = REAL_ONE >> 1
REAL_TWO = REAL_ONE << 1
REAL_LN_TWO = 762123384786
REAL_PI = 3454217652358
REAL_HALF_PI = 1727108826179
REAL_TWO_PI = 6908435304715
REAL_HALF_CIRCLE = 197912092999680
REAL_CIRCLE = 395824185999360
SIGN_MASK = 1 << 127

def toReal(ipart):
    """
    /**
     * Convert an integer to a real. Preserves sign.
     */
    function toReal(int88 ipart) public pure returns (int128) {
        return int128(ipart) * REAL_ONE;
    }
    """
    return int(ipart * REAL_ONE)

def fromReal(real_value):
    """
    /**
     * Convert a real to an integer. Preserves sign.
     */
    function fromReal(int128 real_value) public pure returns (int88) {
        return int88(real_value / REAL_ONE);
    }
    """
    return int(real_value / REAL_ONE)

def round(real_value):
    """
    /**
     * Round a real to the nearest integral real value.
     */
    function round(int128 real_value) public pure returns (int128) {
        // First, truncate.
        int88 ipart = fromReal(real_value);
        if ((fractionalBits(real_value) & (uint40(1) << uint40(REAL_FBITS - 1))) > 0) {
            // High fractional bit is set. Round up.
            if (real_value < int128(0)) {
                // Rounding up for a negative number is rounding down.
                ipart -= 1;
            } else {
                ipart += 1;
            }
        }
        return toReal(ipart);
    }
    """
    ipart = fromReal(real_value)
    if ((fractionalBits(real_value) and (1 << (REAL_FBITS - 1))) > 0):
        if real_value < 0:
            ipart -= 1
        else:
            ipart += 1
    return toReal(ipart)

def abs(real_value):
    """
    /**
     * Get the absolute value of a real. Just the same as abs on a normal int128.
     */
    function abs(int128 real_value) public pure returns (int128) {
        if (real_value > 0) {
            return real_value;
        } else {
            return -real_value;
        }
    }
    """
    if real_value > 0:
        return real_value
    else:
        return -real_value

def fractionalBits(real_value):
    """
    /**
     * Returns the fractional bits of a real. Ignores the sign of the real.
     */
    function fractionalBits(int128 real_value) public pure returns (uint40) {
        return uint40(abs(real_value) % REAL_ONE);
    }
    """
    return int(abs(real_value) % REAL_ONE)

def fpart(real_value):
    """
    /**
     * Get the fractional part of a real, as a real. Ignores sign (so fpart(-0.5) is 0.5).
     */
    function fpart(int128 real_value) public pure returns (int128) {
        // This gets the fractional part but strips the sign
        return abs(real_value) % REAL_ONE;
    }
    """
    return abs(real_value) % REAL_ONE

def fpartSigned(real_value):
    """
    /**
     * Get the fractional part of a real, as a real. Respects sign (so fpartSigned(-0.5) is -0.5).
     */
    function fpartSigned(int128 real_value) public pure returns (int128) {
        // This gets the fractional part but strips the sign
        int128 fractional = fpart(real_value);
        if (real_value < 0) {
            // Add the negative sign back in.
            return -fractional;
        } else {
            return fractional;
        }
    }
    """
    fractional = int(fpart(real_value))
    if real_value < 0:
        return -fractional
    else:
        return fractional

def ipart(real_value):
    """
    /**
     * Get the integer part of a fixed point value.
     */
    function ipart(int128 real_value) public pure returns (int128) {
        // Subtract out the fractional part to get the real part.
        return real_value - fpartSigned(real_value);
    }
    """
    return real_value - fpartSigned(real_value)

def mul(real_a, real_b):
    """
    /**
     * Multiply one real by another. Truncates overflows.
     */
    function mul(int128 real_a, int128 real_b) public pure returns (int128) {
        // When multiplying fixed point in x.y and z.w formats we get (x+z).(y+w) format.
        // So we just have to clip off the extra REAL_FBITS fractional bits.
        return int128((int256(real_a) * int256(real_b)) >> REAL_FBITS);
    }
    """
    return int((int(real_a) * int(real_b)) >> REAL_FBITS)

def div(real_numerator, real_denominator):
    """
    /**
     * Divide one real by another real. Truncates overflows.
     */
    function div(int128 real_numerator, int128 real_denominator) public pure returns (int128) {
        // We use the reverse of the multiplication trick: convert numerator from
        // x.y to (x+z).(y+w) fixed point, then divide by denom in z.w fixed point.
        return int128((int256(real_numerator) * REAL_ONE) / int256(real_denominator));
    }
    """
    return int(int(real_numerator) * REAL_ONE) / int(real_denominator)

def fraction(numerator, denominator):
    """
    /**
     * Create a real from a rational fraction.
     */
    function fraction(int88 numerator, int88 denominator) public pure returns (int128) {
        return div(toReal(numerator), toReal(denominator));
    }
    """
    return div(toReal(numerator), toReal(denominator))

def ipow(real_base, exponent):
    """
    /**
     * Raise a number to a positive integer power in O(log power) time.
     * See <https://stackoverflow.com/a/101613>
     */
    function ipow(int128 real_base, int88 exponent) public pure returns (int128) {
        if (exponent < 0) {
            // Negative powers are not allowed here.
            revert();
        }

        // Start with the 0th power
        int128 real_result = REAL_ONE;
        while (exponent != 0) {
            // While there are still bits set
            if ((exponent & 0x1) == 0x1) {
                // If the low bit is set, multiply in the (many-times-squared) base
                real_result = mul(real_result, real_base);
            }
            // Shift off the low bit
            exponent = exponent >> 1;
            // Do the squaring
            real_base = mul(real_base, real_base);
        }

        // Return the final result.
        return real_result;
    }
    """
    if (exponent < 0):
        raise Exception
    real_result = REAL_ONE
    while (exponent != 0) :
        if ((exponent & 0x1) == 0x1):
            real_result = mul(real_result, real_base)
        exponent = exponent >> 1
        real_base = mul(real_base, real_base)
    return real_result

def hibit(val):
    """
    /**
     * Zero all but the highest set bit of a number.
     * See <https://stackoverflow.com/a/53184>
     */
    function hibit(uint256 val) internal pure returns (uint256) {
        // Set all the bits below the highest set bit
        val |= (val >>  1);
        val |= (val >>  2);
        val |= (val >>  4);
        val |= (val >>  8);
        val |= (val >> 16);
        val |= (val >> 32);
        val |= (val >> 64);
        val |= (val >> 128);
        return val ^ (val >> 1);
    }
    """
    val |= (val >>  1)
    val |= (val >>  2)
    val |= (val >>  4)
    val |= (val >>  8)
    val |= (val >> 16)
    val |= (val >> 32)
    val |= (val >> 64)
    val |= (val >> 128)
    return val ^ (val >> 1)

def findbit(val):
    """
    /**
     * Given a number with one bit set, finds the index of that bit.
     */
    function findbit(uint256 val) internal pure returns (uint8 index) {
        index = 0;
        // We and the value with alternating bit patters of various pitches to find it.

        if (val & 0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA != 0) {
            // Picth 1
            index |= 1;
        }
        if (val & 0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC != 0) {
            // Pitch 2
            index |= 2;
        }
        if (val & 0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0 != 0) {
            // Pitch 4
            index |= 4;
        }
        if (val & 0xFF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00 != 0) {
            // Pitch 8
            index |= 8;
        }
        if (val & 0xFFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000 != 0) {
            // Pitch 16
            index |= 16;
        }
        if (val & 0xFFFFFFFF00000000FFFFFFFF00000000FFFFFFFF00000000FFFFFFFF00000000 != 0) {
            // Pitch 32
            index |= 32;
        }
        if (val & 0xFFFFFFFFFFFFFFFF0000000000000000FFFFFFFFFFFFFFFF0000000000000000 != 0) {
            // Pitch 64
            index |= 64;
        }
        if (val & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000000000000000000000000000 != 0) {
            // Pitch 128
            index |= 128;
        }
    }
    """
    index = 0
    if (val & 0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA != 0) :
        index |= 1
    if (val & 0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC != 0) :
        index |= 2
    if (val & 0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0 != 0) :
        index |= 4
    if (val & 0xFF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00 != 0) :
        index |= 8
    if (val & 0xFFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000 != 0) :
        index |= 16
    if (val & 0xFFFFFFFF00000000FFFFFFFF00000000FFFFFFFF00000000FFFFFFFF00000000 != 0) :
        index |= 32
    if (val & 0xFFFFFFFFFFFFFFFF0000000000000000FFFFFFFFFFFFFFFF0000000000000000 != 0) :
        index |= 64
    if (val & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000000000000000000000000000 != 0) :
        index |= 128

def rescale(real_arg):
    """
    /**
     * Shift real_arg left or right until it is between 1 and 2. Return the
     * rescaled value, and the number of bits of right shift applied. Shift may be negative.
     *
     * Expresses real_arg as real_scaled * 2^shift, setting shift to put real_arg between [1 and 2).
     *
     * Rejects 0 or negative arguments.
     */
    function rescale(int128 real_arg) internal pure returns (int128 real_scaled, int88 shift) {
        if (real_arg <= 0) {
            // Not in domain!
            revert();
        }

        // Find the high bit
        int88 high_bit = findbit(hibit(uint256(real_arg)));

        // We'll shift so the high bit is the lowest non-fractional bit.
        shift = high_bit - int88(REAL_FBITS);

        if (shift < 0) {
            // Shift left
            real_scaled = real_arg << int128(-shift);
        } else if (shift >= 0) {
            // Shift right
            real_scaled = real_arg >> int128(shift);
        }
    }
    """
    if (real_arg <= 0) :
        raise Exception
    high_bit = findbit(hibit(int(real_arg)))
    shift = high_bit - int(REAL_FBITS)
    if (shift < 0) :
        real_scaled = real_arg << int(-shift)
    elif (shift >= 0) :
        real_scaled = real_arg >> int(shift)

def lnLimited(real_arg, max_iterations):
    """
    /**
     * Calculate the natural log of a number. Rescales the input value and uses
     * the algorithm outlined at <https://math.stackexchange.com/a/977836> and
     * the ipow implementation.
     *
     * Lets you artificially limit the number of iterations.
     *
     * Note that it is potentially possible to get an un-converged value; lack
     * of convergence does not throw.
     */
    function lnLimited(int128 real_arg, int max_iterations) public pure returns (int128) {
        if (real_arg <= 0) {
            // Outside of acceptable domain
            revert();
        }

        if (real_arg == REAL_ONE) {
            // Handle this case specially because people will want exactly 0 and
            // not ~2^-39 ish.
            return 0;
        }

        // We know it's positive, so rescale it to be between [1 and 2)
        int128 real_rescaled;
        int88 shift;
        (real_rescaled, shift) = rescale(real_arg);

        // Compute the argument to iterate on
        int128 real_series_arg = div(real_rescaled - REAL_ONE, real_rescaled + REAL_ONE);

        // We will accumulate the result here
        int128 real_series_result = 0;

        for (int88 n = 0; n < max_iterations; n++) {
            // Compute term n of the series
            int128 real_term = div(ipow(real_series_arg, 2 * n + 1), toReal(2 * n + 1));
            // And add it in
            real_series_result += real_term;
            if (real_term == 0) {
                // We must have converged. Next term is too small to represent.
                break;
            }
            // If we somehow never converge I guess we will run out of gas
        }

        // Double it to account for the factor of 2 outside the sum
        real_series_result = mul(real_series_result, REAL_TWO);

        // Now compute and return the overall result
        return mul(toReal(shift), REAL_LN_TWO) + real_series_result;

    }
    """
    if (real_arg <= 0) :
        raise Exception
    if (real_arg == REAL_ONE) :
        return 0
    (real_rescaled, shift) = rescale(real_arg)
    real_series_arg = div(real_rescaled - REAL_ONE, real_rescaled + REAL_ONE)
    real_series_result = 0
    # for (n = 0 n < max_iterations n++) :
    for n in range(max_iterations):
        real_term = div(ipow(real_series_arg, 2 * n + 1), toReal(2 * n + 1))
        real_series_result += real_term
        if (real_term == 0) :
            break
    real_series_result = mul(real_series_result, REAL_TWO)
    return mul(toReal(shift), REAL_LN_TWO) + real_series_result

def ln(real_arg):
    """
    /**
     * Calculate a natural logarithm with a sensible maximum iteration count to
     * wait until convergence. Note that it is potentially possible to get an
     * un-converged value; lack of convergence does not throw.
     */
    function ln(int128 real_arg) public pure returns (int128) {
        return lnLimited(real_arg, 100);
    }
    """
    return lnLimited(real_arg, 100)

def expLimited(real_arg, max_iterations):
    """
    /**
     * Calculate e^x. Uses the series given at
     * <http://pages.mtu.edu/~shene/COURSES/cs201/NOTES/chap04/exp.html>.
     *
     * Lets you artificially limit the number of iterations.
     *
     * Note that it is potentially possible to get an un-converged value; lack
     * of convergence does not throw.
     */
    function expLimited(int128 real_arg, int max_iterations) public pure returns (int128) {
        // We will accumulate the result here
        int128 real_result = 0;

        // We use this to save work computing terms
        int128 real_term = REAL_ONE;

        for (int88 n = 0; n < max_iterations; n++) {
            // Add in the term
            real_result += real_term;

            // Compute the next term
            real_term = mul(real_term, div(real_arg, toReal(n + 1)));

            if (real_term == 0) {
                // We must have converged. Next term is too small to represent.
                break;
            }
            // If we somehow never converge I guess we will run out of gas
        }

        // Return the result
        return real_result;

    }
    """
    real_result = 0
    real_term = REAL_ONE
    for n in range(max_iterations):
        real_result += real_term
        real_term = mul(real_term, div(real_arg, toReal(n + 1)))
        if (real_term == 0) :
            break
    return real_result

def exp(real_arg):
    """
    /**
     * Calculate e^x with a sensible maximum iteration count to wait until
     * convergence. Note that it is potentially possible to get an un-converged
     * value; lack of convergence does not throw.
     */
    function exp(int128 real_arg) public pure returns (int128) {
        return expLimited(real_arg, 100);
    }
    """
    return expLimited(real_arg, 100)

def pow(real_base, real_exponent):
    """
    /**
     * Raise any number to any power, except for negative bases to fractional powers.
     */
    function pow(int128 real_base, int128 real_exponent) public pure returns (int128) {
        if (real_exponent == 0) {
            // Anything to the 0 is 1
            return REAL_ONE;
        }

        if (real_base == 0) {
            if (real_exponent < 0) {
                // Outside of domain!
                revert();
            }
            // Otherwise it's 0
            return 0;
        }

        if (fpart(real_exponent) == 0) {
            // Anything (even a negative base) is super easy to do to an integer power.

            if (real_exponent > 0) {
                // Positive integer power is easy
                return ipow(real_base, fromReal(real_exponent));
            } else {
                // Negative integer power is harder
                return div(REAL_ONE, ipow(real_base, fromReal(-real_exponent)));
            }
        }

        if (real_base < 0) {
            // It's a negative base to a non-integer power.
            // In general pow(-x^y) is undefined, unless y is an int or some
            // weird rational-number-based relationship holds.
            revert();
        }

        // If it's not a special case, actually do it.
        return exp(mul(real_exponent, ln(real_base)));
    }
    """
    if (real_exponent == 0):
        return REAL_ONE
    if (real_base == 0):
        if (real_exponent < 0):
            raise Exception
        return 0
    if (fpart(real_exponent) == 0):
        if (real_exponent > 0):
            return ipow(real_base, fromReal(real_exponent))
        else :
            return div(REAL_ONE, ipow(real_base, fromReal(-real_exponent)))
    if (real_base < 0):
        raise Exception
    return exp(mul(real_exponent, ln(real_base)))

def sqrt(real_arg):
    """
    /**
     * Compute the square root of a number.
     */
    function sqrt(int128 real_arg) public pure returns (int128) {
        return pow(real_arg, REAL_HALF);
    }
    """
    return pow(real_arg, REAL_HALF)

def sinLimited(real_arg, max_iterations):
    """
    /**
     * Compute the sin of a number to a certain number of Taylor series terms.
     */
    function sinLimited(int128 real_arg, int88 max_iterations) public pure returns (int128) {
        // First bring the number into 0 to 2 pi
        // TODO: This will introduce an error for very large numbers, because the error in our Pi will compound.
        // But for actual reasonable angle values we should be fine.
        real_arg = real_arg % REAL_TWO_PI;

        int128 accumulator = REAL_ONE;

        // We sum from large to small iteration so that we can have higher powers in later terms
        for (int88 iteration = max_iterations - 1; iteration >= 0; iteration--) {
            accumulator = REAL_ONE - mul(div(mul(real_arg, real_arg), toReal((2 * iteration + 2) * (2 * iteration + 3))), accumulator);
            // We can't stop early; we need to make it to the first term.
        }

        return mul(real_arg, accumulator);
    }
    """
    real_arg = real_arg % REAL_TWO_PI
    accumulator = REAL_ONE
    # for (iteration = max_iterations - 1 iteration >= 0 iteration--) :
    for i in range(max_iterations - 1, -1, -1):
        accumulator = REAL_ONE - mul(div(mul(real_arg, real_arg), toReal((2 * i + 2) * (2 * i + 3))), accumulator)
    return mul(real_arg, accumulator)

def sin(real_arg):
    """
    /**
     * Calculate sin(x) with a sensible maximum iteration count to wait until
     * convergence.
     */
    function sin(int128 real_arg) public pure returns (int128) {
        return sinLimited(real_arg, 15);
    }
    """
    return sinLimited(real_arg, 15)

def cos(real_arg):
    """
    /**
     * Calculate cos(x).
     */
    function cos(int128 real_arg) public pure returns (int128) {
        return sin(real_arg + REAL_HALF_PI);
    }
    """
    return sin(real_arg + REAL_HALF_PI)

def tan(real_arg):
    """
    /**
     * Calculate tan(x). May overflow for large results. May throw if tan(x)
     * would be infinite, or return an approximation, or overflow.
     */
    function tan(int128 real_arg) public pure returns (int128) {
        return div(sin(real_arg), cos(real_arg));
    }
    """
    return div(sin(real_arg), cos(real_arg))

def atanSmall(real_arg):
    """
    /**
     * Calculate atan(x) for x in [-1, 1].
     * Uses the Chebyshev polynomial approach presented at
     * https://www.mathworks.com/help/fixedpoint/examples/calculate-fixed-point-arctangent.html
     * Uses polynomials received by personal communication.
     * 0.999974x-0.332568x^3+0.193235x^5-0.115729x^7+0.0519505x^9-0.0114658x^11
     */
    function atanSmall(int128 real_arg) public pure returns (int128) {
        int128 real_arg_squared = mul(real_arg, real_arg);
        return mul(mul(mul(mul(mul(mul(
            - 12606780422,  real_arg_squared) // x^11
            + 57120178819,  real_arg_squared) // x^9
            - 127245381171, real_arg_squared) // x^7
            + 212464129393, real_arg_squared) // x^5
            - 365662383026, real_arg_squared) // x^3
            + 1099483040474, real_arg);       // x^1
    }
    """
    real_arg_squared = mul(real_arg, real_arg)
    return mul(mul(mul(mul(mul(mul(- 12606780422,  real_arg_squared) + 57120178819,  real_arg_squared) - 127245381171, real_arg_squared) + 212464129393, real_arg_squared) - 365662383026, real_arg_squared) + 1099483040474, real_arg)

def atan2(real_y, real_x):
    """
    /**
     * Compute the nice two-component arctangent of y/x.
     */
    function atan2(int128 real_y, int128 real_x) public pure returns (int128) {
        int128 atan_result;

        // Do the angle correction shown at
        // https://www.mathworks.com/help/fixedpoint/examples/calculate-fixed-point-arctangent.html

        // We will re-use these absolute values
        int128 real_abs_x = abs(real_x);
        int128 real_abs_y = abs(real_y);

        if (real_abs_x > real_abs_y) {
            // We are in the (0, pi/4] region
            // abs(y)/abs(x) will be in 0 to 1.
            atan_result = atanSmall(div(real_abs_y, real_abs_x));
        } else {
            // We are in the (pi/4, pi/2) region
            // abs(x) / abs(y) will be in 0 to 1; we swap the arguments
            atan_result = REAL_HALF_PI - atanSmall(div(real_abs_x, real_abs_y));
        }

        // Now we correct the result for other regions
        if (real_x < 0) {
            if (real_y < 0) {
                atan_result -= REAL_PI;
            } else {
                atan_result = REAL_PI - atan_result;
            }
        } else {
            if (real_y < 0) {
                atan_result = -atan_result;
            }
        }

        return atan_result;
    }
    """
    atan_result
    real_abs_x = abs(real_x)
    real_abs_y = abs(real_y)
    if (real_abs_x > real_abs_y):
        atan_result = atanSmall(div(real_abs_y, real_abs_x))
    else:
        atan_result = REAL_HALF_PI - atanSmall(div(real_abs_x, real_abs_y))
    if (real_x < 0):
        if (real_y < 0):
            atan_result -= REAL_PI
        else:
            atan_result = REAL_PI - atan_result
    else:
        if (real_y < 0):
            atan_result = -atan_result
    return atan_result

def realRadianToDegree(realRadian):
    return div(mul(realRadian, REAL_HALF_CIRCLE), REAL_PI)

def realDegreeToRadian(realDegree):
    return div(mul(realDegree, REAL_PI), REAL_HALF_CIRCLE)
