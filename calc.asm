org  0x100                   ; Start of a .COM program

section .data
    a db 5                   ; Define a = 5
    b db 3                   ; Define b = 3
    c db 2                   ; Define c = 2
    resultMsg db 'Result: ', 0 ; Reserve space for the rest of the message

section .text
_start:
    mov al, [b]              ; Load b into al
    sub al, [c]              ; Subtract c from al
    add al, [a]              ; Add a to al

    ; Convert result to ASCII character (for single-digit numbers)
    add al, '0'              ; Convert number to ASCII character

    ; Store result into the message at the correct position
    mov [resultMsg+8], al    ; Store result in the message right after 'Result: '
    mov byte [resultMsg+9], '$' ; Set termination character for DOS output

    ; Print the message
    mov ah, 09h              ; DOS function to print a string
    lea dx, resultMsg        ; Set DX to the address of resultMsg
    int 21h                  ; Call DOS interrupt

    ; Terminate the program
    mov ax, 4c00h            ; DOS function to end program
    int 21h                  ; Call DOS interrupt
