module example
    use iso_c_binding
    implicit none
contains
    subroutine sqr_2d_arr_int(nd, val) BIND(C, NAME = 'sqr_2d_arr_int')
        !DEC$ ATTRIBUTES DLLEXPORT :: sqr_2d_arr
        integer, intent(in) :: nd
        integer, intent(inout) :: val(nd, nd)
        integer :: i, j
        do j = 1, nd
            do i = 1, nd
                val(i, j) = val(i, j) ** 2
            enddo
        enddo
    end subroutine sqr_2d_arr_int

    subroutine sqr_2d_arr_real(nd, val) BIND(C, NAME = 'sqr_2d_arr_real')
        !DEC$ ATTRIBUTES DLLEXPORT :: sqr_2d_arr
        integer, intent(in) :: nd
        real(kind = c_double), intent(inout) :: val(nd, nd)
        integer :: i, j
        do j = 1, nd
            do i = 1, nd
                val(i, j) = val(i, j) * val(i,j)
            enddo
        enddo
    end subroutine sqr_2d_arr_real
end module example