;rekurzív faktoriális
(define (faktorialis n)(if (< n 1)1(* n (faktorialis (- n 1)))))
;faktorialis
;> (faktorialis 5)
;120
