module example
    use iso_c_binding
    implicit none
contains
    subroutine sqr_2d_arr_int(nd1, nd2, val) BIND(C, NAME = 'sqr_2d_arr_int')
        !DEC$ ATTRIBUTES DLLEXPORT :: sqr_2d_arr
        integer, intent(in) :: nd1
        integer, intent(in) :: nd2
        integer, intent(inout) :: val(nd1, nd2)
        integer :: i, j
        do j = 1, nd2
            do i = 1, nd1
                val(i, j) = val(i, j) ** 2
            enddo
        enddo
    end subroutine sqr_2d_arr_int

    subroutine sqr_2d_arr_real(nd1, nd2, val) BIND(C, NAME = 'sqr_2d_arr_real')
        !DEC$ ATTRIBUTES DLLEXPORT :: sqr_2d_arr
        integer(kind = c_int), intent(in) :: nd1
        integer, intent(in) :: nd2
        real(kind = c_double), intent(inout) :: val(nd1, nd2)
        integer :: i, j

        print*, 'nd1', nd1
        print*, 'nd2', nd2
        print*, 'val 1', val(:,1)
        do j = 1, nd2
            do i = 1, nd1
                val(i, j) = val(i, j) * val(i,j)
            enddo
        enddo
    end subroutine sqr_2d_arr_real
end module example