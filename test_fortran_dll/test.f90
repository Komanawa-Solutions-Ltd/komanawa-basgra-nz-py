subroutine sqr2(val) BIND(C, NAME='sqr2')
    use iso_c_binding
    !DEC$ ATTRIBUTES DLLEXPORT :: sqr2
    integer, intent(inout) :: val
    val = val ** 2
end subroutine sqr2