cmake_minimum_required(VERSION 3.12)
project(ImageMagick)

#
# OPTIONS
#

option(shared "ON, OFF" ON)
#option(quantumDepth "8, 16, 32" 16)
option(openmp "ON, OFF" ON)
option(opencl "ON, OFF" ON)
option(largefile "ON, OFF" ON)
option(hdri "ON, OFF" ON)
option(deprecated "ON, OFF" ON)
option(cipher "ON, OFF" ON)
option(zeroConfiguration "ON, OFF" ON)
option(docs "ON, OFF" ON)
option(threads "ON, OFF" ON)
option(bzlib "ON, OFF" ON)
option(x "ON, OFF" ON)
option(dps "ON, OFF" ON)
option(fftw "ON, OFF" ON)
option(flif "ON, OFF" ON)
option(fpx "ON, OFF" ON)
option(djvu "ON, OFF" ON)
option(raqm "ON, OFF" ON)
option(heic "ON, OFF" ON)
option(jbig "ON, OFF" ON)
option(lcms "ON, OFF" ON)
option(lqr "ON, OFF" ON)
option(openexr "ON, OFF" ON)
option(pango "ON, OFF" ON)
option(webp "ON, OFF" ON)
option(wmf "ON, OFF" ON)
option(fontconfig "ON, OFF" ON)
option(freetype "ON, OFF" ON)
option(openjp2 "ON, OFF" ON)
option(gslib "ON, OFF" OFF)
option(gvc "ON, OFF" OFF)
option(rsvg "ON, OFF" OFF)
option(wmf "ON, OFF" OFF)
option(jpeg "ON, OFF" ON)
option(png "ON, OFF" ON)
option(xml "ON, OFF" ON)
option(zlib "ON, OFF" ON)
option(lzma "ON, OFF" ON)
option(tiff "ON, OFF" ON)

set(sharedOrStatic "STATIC")
if(shared)
	set(sharedOrStatic "SHARED")
endif(shared)

if(NOT DEFINED quantumDepth)
	set(quantumDepth 16)
endif(NOT DEFINED quantumDepth)

#
# Configure config.
#

if(opencl)
	set(MAGICKCORE__OPENCL "")
	set(MAGICKCORE_HAVE_CL_CL_H "")
	add_compile_definitions(MAGICKCORE__OPENCL)
	add_compile_definitions(MAGICKCORE_HAVE_CL_CL_H)
endif(opencl)

if(hdri)
	set(MAGICKCORE_HDRI_ENABLE 1)
else(hdri)
	set(MAGICKCORE_HDRI_ENABLE 0)
endif(hdri)
add_compile_definitions(MAGICKCORE_HDRI_ENABLE=${MAGICKCORE_HDRI_ENABLE})

if(deprecated)
	set(MAGICKCORE_EXCLUDE_DEPRECATED "")
	add_compile_definitions(MAGICKCORE_EXCLUDE_DEPRECATED)
endif(deprecated)

if(zeroConfiguration)
	set(MAGICKCORE_ZERO_CONFIGURATION_SUPPORT "")
	add_compile_definitions(MAGICKCORE_ZERO_CONFIGURATION_SUPPORT)
endif(zeroConfiguration)

if(bzlib)
	set(MAGICKCORE_BZLIB_DELEGATE "")
	add_compile_definitions(MAGICKCORE_BZLIB_DELEGATE)
endif(bzlib)
	
if(jpeg)
	set(MAGICKCORE_JPEG_DELEGATE "")
	add_compile_definitions(MAGICKCORE_JPEG_DELEGATE)
endif(jpeg)
	
if(lcms)
	set(MAGICKCORE_LCMS_DELEGATE "")
	set(MAGICKCORE_HAVE_LCMS2_H "")
	add_compile_definitions(MAGICKCORE_LCMS_DELEGATE)
	add_compile_definitions(MAGICKCORE_HAVE_LCMS2_H)
endif(lcms)
	
if(xml)
	set(MAGICKCORE_XML_DELEGATE "")
	add_compile_definitions(MAGICKCORE_XML_DELEGATE)
endif(xml)
	
if(lqr)
	set(MAGICKCORE_LQR_DELEGATE "")
	add_compile_definitions(MAGICKCORE_LQR_DELEGATE)
endif(lqr)
	
if(png)
	set(MAGICKCORE_PNG_DELEGATE "")
	add_compile_definitions(MAGICKCORE_PNG_DELEGATE)
endif(png)
	
if(tiff)
	set(MAGICKCORE_TIFF_DELEGATE "")
	set(MAGICKCORE_HAVE_TIFFCONF_H "")
	add_compile_definitions(MAGICKCORE_TIFF_DELEGATE)
	add_compile_definitions(MAGICKCORE_HAVE_TIFFCONF_H)
endif(tiff)
	
if(freetype)
	set(MAGICKCORE_FREETYPE_DELEGATE "")
	add_compile_definitions(MAGICKCORE_FREETYPE_DELEGATE)
endif(freetype)
	
if(zlib)
	set(MAGICKCORE_ZLIB_DELEGATE "")
	add_compile_definitions(MAGICKCORE_ZLIB_DELEGATE)
endif(zlib)

configure_file(magick-baseconfig.h.in ${CMAKE_CURRENT_SOURCE_DIR}/MagickCore/magick-baseconfig.h @ONLY)

#
# Configure version
#

set(PACKAGE_NAME "ImageMagick")
set(PACKAGE_LIB_VERSION "0x707")
set(MAGICK_LIB_VERSION_TEXT "7.0.7")
set(MAGICK_LIB_VERSION_NUMBER "7,0,7,22")
set(PACKAGE_VERSION_ADDENDUM "-22")
set(MAGICK_LIBRARY_CURRENT "5")
set(MAGICK_LIBRARY_CURRENT_MIN "0")
set(PACKAGE_RELEASE_DATE "")

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/MagickCore/version.h.in ${CMAKE_CURRENT_SOURCE_DIR}/MagickCore/version.h @ONLY)

#
# Conan
#
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

#
# Definitions
#
add_compile_definitions(
	_MAGICKLIB_
	_MAGICKMOD_
)

if(shared)
	add_compile_definitions(_DLL)
else()
	add_compile_definitions(_LIB)
endif(shared)

#
# MagickCore
#

file(GLOB_RECURSE core_headers MagickCore/*.h)
file(GLOB_RECURSE core_sources MagickCore/*.c)

set(core_coders "")
set(core_targets "")

if(bzlib OR WIN32)
	list(APPEND core_targets PRIVATE CONAN_PKG::bzip2)
endif(bzlib OR WIN32)

if(WIN32)
	list(APPEND core_targets PRIVATE CONAN_PKG::glib)
endif(WIN32)

if(lcms OR WIN32)
	list(APPEND core_targets PRIVATE CONAN_PKG::lcms)
endif(lcms OR WIN32)

if(zlib OR png OR tiff OR WIN32)
	list(APPEND core_targets PRIVATE CONAN_PKG::zlib)
endif(bzlib OR WIN32)

if(lqr OR WIN32)
	list(APPEND core_targets PRIVATE CONAN_PKG::lqr)
endif(lqr OR WIN32)

if(freetype OR WIN32)
	list(APPEND core_targets PRIVATE CONAN_PKG::freetype)
	list(APPEND core_coders coders/ttf.c)
endif(freetype OR WIN32)

if(jpeg)
	list(APPEND core_targets PRIVATE CONAN_PKG::libjpeg-turbo)
	list(APPEND core_coders coders/jpeg.c)
endif(jpeg)

if(png)
	list(APPEND core_targets PRIVATE CONAN_PKG::libpng)
	list(APPEND core_coders coders/png.c)
endif(png)

if(xml)
	list(APPEND core_targets PRIVATE CONAN_PKG::libxml2)
endif(xml)

if(lzma)
	list(APPEND core_targets PRIVATE CONAN_PKG::lzma)
endif(lzma)

if(tiff)
	list(APPEND core_coders coders/psd.c)
endif(tiff)

if(tiff)
	list(APPEND core_targets PRIVATE CONAN_PKG::libtiff)
	list(APPEND core_coders coders/tiff.c)
endif(tiff)


source_group(
	TREE ${CMAKE_CURRENT_SOURCE_DIR}
	PREFIX core_src
	FILES ${core_headers} ${core_sources} ${core_coders}
)

add_library(MagickCore ${sharedOrStatic}
	${core_headers}
	${core_sources}
	${core_coders}
)
set_target_properties(MagickCore PROPERTIES OUTPUT_NAME "MagickCore-7.Q${quantumDepth}")

target_link_libraries(MagickCore
	${core_targets}
)

target_include_directories(MagickCore
	PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/coders
	PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/MagickCore
	PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}
)

#
# MagickWand
#

file(GLOB wand_headers MagickWand/*.h)
file(GLOB wand_sources MagickWand/*.c)

source_group(
	TREE ${CMAKE_CURRENT_SOURCE_DIR}
	PREFIX wand_src
	FILES ${wand_headers} ${wand_sources}
)

add_library(MagickWand ${sharedOrStatic}
	${wand_headers}
	${wand_sources}
)
set_target_properties(MagickWand PROPERTIES OUTPUT_NAME "MagickWand-7.Q${quantumDepth}")

target_link_libraries(MagickWand
	PRIVATE MagickCore
)

target_include_directories(MagickWand
	PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/MagickWand
)

#
# Magick++
#

file(GLOB_RECURSE plusplus_headers Magick++/lib/*.h)
file(GLOB_RECURSE plusplus_sources Magick++/lib/*.cpp)

source_group(
	TREE ${CMAKE_CURRENT_SOURCE_DIR}
	PREFIX plusplus_src
	FILES ${plusplus_headers} ${plusplus_sources}
)

add_library(MagickPlusPlus ${sharedOrStatic}
	${plusplus_headers}
	${plusplus_sources}
)
set_target_properties(MagickPlusPlus PROPERTIES OUTPUT_NAME "Magick++-7.Q${quantumDepth}")

target_link_libraries(MagickPlusPlus
	PRIVATE MagickCore
	PRIVATE MagickWand
)

target_include_directories(MagickPlusPlus
	PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/Magick++/lib
)
