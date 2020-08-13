module example
    use iso_c_binding
    implicit none
contains
    subroutine sqr_2d_arr(nd, val) BIND(C, NAME='sqr_2d_arr')
        !DEC$ ATTRIBUTES DLLEXPORT :: sqr_2d_arr
        integer, intent(in) :: nd
        integer, intent(inout) :: val(nd, nd)
        integer :: i, j
        do j = 1, nd
        do i = 1, nd
            val(i, j) = (val(i, j) + val(j, i)) ** 2
        enddo
        enddo
    end subroutine sqr_2d_arr
end module example