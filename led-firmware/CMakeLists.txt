cmake_minimum_required(VERSION 3.15)
project(LEDFirmware C ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS_INIT "-mcpu=cortex-m4 -mthumb -Wall -Wextra")

# Directories
include_directories(${CMAKE_SOURCE_DIR}/include)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

# Test executable (host target)
add_executable(led_test
    tests/led_test.c
    src/led.c
)
set_target_properties(led_test PROPERTIES EXCLUDE_FROM_ALL TRUE)
target_include_directories(led_test PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_compile_options(led_test PRIVATE -std=c99 -Wall -Wextra)

# Firmware executable (bare metal)
add_executable(firmware.elf
    src/startup.c
    src/main.c
    src/led.c
)

target_compile_options(firmware.elf PRIVATE
    -mcpu=cortex-m4
    -mthumb
    -ffreestanding
    -fno-common
    -O2
)

# Link with linker script
target_link_options(firmware.elf PRIVATE
    -mcpu=cortex-m4
    -mthumb
    -nostdlib
    -nostartfiles
    -Wl,--gc-sections
    -Wl,-Map=${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/firmware.map
    -T${CMAKE_SOURCE_DIR}/linker.ld
)

# Object copy to generate HEX and BIN
find_program(OBJCOPY NAMES arm-none-eabi-objcopy REQUIRED)
find_program(OBJDUMP NAMES arm-none-eabi-objdump REQUIRED)

add_custom_command(
    TARGET firmware.elf POST_BUILD
    COMMAND ${OBJCOPY} -O ihex $<TARGET_FILE:firmware.elf> ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/firmware.hex
    COMMAND ${OBJCOPY} -O binary $<TARGET_FILE:firmware.elf> ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/firmware.bin
    COMMAND ${OBJDUMP} -h $<TARGET_FILE:firmware.elf>
    COMMENT "Generating firmware HEX and BIN files"
)
