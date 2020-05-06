#!/usr/bin/clisp

(defun factorial_iterative (n)
	(let ((f 1))
		(dotimes (i n)
		(setf f (* f (+ i 1))))
		f
	)
)

(defun factorial_recursive (n)
  (if (= n 0)
      1
      (* n (factorial_recursive (- n 1))) ) )

(format t "Recursive:~%")

(loop for i from 0 to 20
	do (format t "~D! = ~D~%" i (factorial_recursive i)) )

(format t "Iterative:~%")

(loop for i from 0 to 20
	do (format t "~D! = ~D~%" i (factorial_iterative i)) )

