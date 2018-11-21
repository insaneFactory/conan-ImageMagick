from conans import ConanFile, AutoToolsBuildEnvironment, CMake, tools
import shutil, os

class ImageMagickConan(ConanFile):
	name = "ImageMagick"
	version = "7.0.7-22"
	license = "ImageMagick License"
	url = "https://github.com/insaneFactory/conan-imagemagick"
	description = "ImageMagick® is a software suite to create, edit, compose, or convert bitmap images. It can read and write images in a variety of formats (over 200) including PNG, JPEG, GIF, HEIC, TIFF, DPX, EXR, WebP, Postscript, PDF, and SVG. Use ImageMagick to resize, flip, mirror, rotate, distort, shear and transform images, adjust image colors, apply various special effects, or draw text, lines, polygons, ellipses and Bézier curves."
	requires = ()
	settings = "os", "compiler", "build_type", "arch"
	exports_sources = "CMakeLists.txt", "magick-baseconfig.h.in"
	generators = "cmake"
	source_subfolder = "src"
	options = {
		"shared": [True, False],
		"quantum-depth": [8, 16, 32],
		"openmp": [True, False],
		"opencl": [True, False],
		"largefile": [True, False],
		"hdri": [True, False],
		"deprecated": [True, False],
		"cipher": [True, False],
		"zero-configuration": [True, False],
		"docs": [True, False],
		"threads": [True, False],
		"bzlib": [True, False],
		"x": [True, False],
		"dps": [True, False],
		"fftw": [True, False],
		"flif": [True, False],
		"fpx": [True, False],
		"djvu": [True, False],
		"raqm": [True, False],
		"heic": [True, False],
		"jbig": [True, False],
		"lcms": [True, False],
		"lqr": [True, False],
		"openexr": [True, False],
		"pango": [True, False],
		"webp": [True, False],
		"wmf": [True, False],
		"fontconfig": [True, False],
		"freetype": [True, False],
		"openjp2": [True, False],
		"dmalloc": [True, False],
		"jemalloc": [True, False],
		"umem": [True, False],
		"autotrace": [True, False],
		"gslib": [True, False],
		"gvc": [True, False],
		"rsvg": [True, False],
		"wmf": [True, False],
		"jpeg": [True, False],
		"png": [True, False],
		"xml": [True, False],
		"zlib": [True, False],
		#"ltdl": [True, False],
		"lzma": [True, False],
		"tiff": [True, False]
	}
	default_options = {
		"shared": True,
		"quantum-depth": 16,
		"openmp": True,
		"opencl": True,
		"largefile": True,
		"hdri": True,
		"deprecated": True,
		"cipher": True,
		"zero-configuration": True,
		"docs": True,
		"threads": True,
		"bzlib": True,
		"x": True,
		"dps": True,
		"fftw": True,
		"flif": True,
		"fpx": True,
		"djvu": True,
		"raqm": True,
		"heic": True,
		"jbig": True,
		"lcms": True,
		"lqr": True,
		"openexr": True,
		"pango": True,
		"webp": True,
		"wmf": True,
		"fontconfig": True,
		"freetype": True,
		"openjp2": True,
		"dmalloc": False,
		"jemalloc": False,
		"umem": False,
		"autotrace": False,
		"gslib": False,
		"gvc": False,
		"rsvg": False,
		"wmf": False,
		"jpeg": True,
		"png": True,
		"xml": True,
		"zlib": True,
		"lzma": True,
		"tiff": True
	}
	
	
	def configure(self):
		if self.settings.os == "Windows":
			self.options.bzlib = True
			#self.options.glib = True
			self.options.lcms = True
			self.options.lqr = True
			self.options.freetype = True
			self.options.zlib = True
			
			del self.options.dmalloc
			del self.options.jemalloc
			del self.options.umem
			del self.options.autotrace
	
	
	def requirements(self):
		if self.settings.os == "Windows" or self.options.bzlib:
			self.requires("bzip2/1.0.6@conan/stable")
		if self.settings.os == "Windows": # or self.options.glib:
			self.requires("glib/2.58.1@insanefactory/stable")
		if self.settings.os == "Windows" or self.options.lcms:
			self.requires("lcms/2.9@bincrafters/stable")
		if self.settings.os == "Windows" or self.options.lqr:
			self.requires("lqr/0.4.2@insanefactory/stable")
		if self.settings.os == "Windows" or self.options.freetype:
			self.requires("freetype/2.9.0@bincrafters/stable")
		if self.settings.os == "Windows" or self.options.zlib:
			self.requires("zlib/1.2.11@conan/stable")
			
		if self.options.jpeg:
			self.requires("libjpeg-turbo/1.5.2@bincrafters/stable")
		if self.options.png:
			self.requires("libpng/1.6.34@bincrafters/stable")
		if self.options.xml:
			self.requires("libxml2/2.9.8@bincrafters/stable")
		if self.options.lzma:
			self.requires("lzma/5.2.4@bincrafters/stable")
		if self.options.tiff:
			self.requires("libtiff/4.0.9@bincrafters/stable")
		

	def source(self):
		self.run("git clone https://github.com/ImageMagick/ImageMagick.git " + self.source_subfolder)
		self.run("cd %s && git fetch --all --tags --prune && git checkout tags/%s" % (self.source_subfolder, self.version))
		shutil.move("CMakeLists.txt", self.source_subfolder + "/CMakeLists.txt")
		shutil.move("magick-baseconfig.h.in", self.source_subfolder + "/magick-baseconfig.h.in")


	def build(self):
		if self.settings.os == "Windows":
			cmake = CMake(self)
			cmake.definitions["shared"] = self.options.shared
			cmake.definitions["quantum-depth"] = str(getattr(self.options, "quantum-depth"))
			cmake.definitions["openmp"] = self.options.openmp
			cmake.definitions["opencl"] = self.options.opencl
			cmake.definitions["largefile"] = self.options.largefile
			cmake.definitions["hdri"] = self.options.hdri
			cmake.definitions["deprecated"] = self.options.deprecated
			cmake.definitions["cipher"] = self.options.cipher
			cmake.definitions["zero-configuration"] = getattr(self.options, "zero-configuration")
			cmake.definitions["docs"] = self.options.docs
			cmake.definitions["threads"] = self.options.threads
			cmake.definitions["bzlib"] = self.options.bzlib
			cmake.definitions["x"] = self.options.x
			cmake.definitions["dps"] = self.options.dps
			cmake.definitions["fftw"] = self.options.fftw
			cmake.definitions["flif"] = self.options.flif
			cmake.definitions["fpx"] = self.options.fpx
			cmake.definitions["djvu"] = self.options.djvu
			cmake.definitions["raqm"] = self.options.raqm
			cmake.definitions["heic"] = self.options.heic
			cmake.definitions["jbig"] = self.options.jbig
			cmake.definitions["lcms"] = self.options.lcms
			cmake.definitions["lqr"] = self.options.lqr
			cmake.definitions["openexr"] = self.options.openexr
			cmake.definitions["pango"] = self.options.pango
			cmake.definitions["webp"] = self.options.webp
			cmake.definitions["wmf"] = self.options.wmf
			cmake.definitions["fontconfig"] = self.options.fontconfig
			cmake.definitions["freetype"] = self.options.freetype
			cmake.definitions["openjp2"] = self.options.openjp2
			cmake.definitions["gslib"] = self.options.gslib
			cmake.definitions["gvc"] = self.options.gvc
			cmake.definitions["rsvg"] = self.options.rsvg
			cmake.definitions["wmf"] = self.options.wmf
			cmake.definitions["jpeg"] = self.options.jpeg
			cmake.definitions["png"] = self.options.png
			cmake.definitions["xml"] = self.options.xml
			cmake.definitions["zlib"] = self.options.zlib
			cmake.definitions["lzma"] = self.options.lzma
			cmake.definitions["tiff"] = self.options.tiff
			cmake.configure(source_folder=self.source_subfolder)
			cmake.build()
		else:
			autotools = AutoToolsBuildEnvironment(self)
			with tools.chdir(builddir):
				args = [
					"--enable-shared=%s" % ("yes" if self.options.shared else "no"),
					"--enable-static=%s" % ("no" if self.options.shared else "yes"),
					"--with-quantum-depth=%s" % str(getattr(self.options, "quantum-depth")),
					"--enable-openmp=%s" % ("yes" if self.options.openmp else "no"),
					"--enable-opencl=%s" % ("yes" if self.options.opencl else "no"),
					"--enable-hdri=%s" % ("yes" if self.options.hdri else "no"),
					"--enable-deprecated=%s" % ("yes" if self.options.deprecated else "no"),
					"--enable-cipher=%s" % ("yes" if self.options.cipher else "no"),
					"--enable-zero-configuration=%s" % ("yes" if getattr(self.options, "zero-configuration") else "no"),
					"--enable-docs=%s" % ("yes" if self.options.docs else "no"),
					"--with-threads=%s" % ("yes" if self.options.threads else "no"),
					"--with-bzlib=%s" % ("yes" if self.options.bzlib else "no"),
					"--with-x=%s" % ("yes" if self.options.x else "no"),
					"--with-dps=%s" % ("yes" if self.options.dps else "no"),
					"--with-fftw=%s" % ("yes" if self.options.fftw else "no"),
					"--with-flif=%s" % ("yes" if self.options.flif else "no"),
					"--with-fpx=%s" % ("yes" if self.options.fpx else "no"),
					"--with-djvu=%s" % ("yes" if self.options.djvu else "no"),
					"--with-raqm=%s" % ("yes" if self.options.raqm else "no"),
					"--with-heic=%s" % ("yes" if self.options.heic else "no"),
					"--with-jbig=%s" % ("yes" if self.options.jbig else "no"),
					"--with-lcms=%s" % ("yes" if self.options.lcms else "no"),
					"--with-lqr=%s" % ("yes" if self.options.lqr else "no"),
					"--with-openexr=%s" % ("yes" if self.options.openexr else "no"),
					"--with-pango=%s" % ("yes" if self.options.pango else "no"),
					"--with-webp=%s" % ("yes" if self.options.webp else "no"),
					"--with-wmf=%s" % ("yes" if self.options.wmf else "no"),
					"--with-fontconfig=%s" % ("yes" if self.options.fontconfig else "no"),
					"--with-freetype=%s" % ("yes" if self.options.freetype else "no"),
					"--with-openjp2=%s" % ("yes" if self.options.openjp2 else "no"),
					"--with-dmalloc=%s" % ("yes" if self.options.dmalloc else "no"),
					"--with-jemalloc=%s" % ("yes" if self.options.jemalloc else "no"),
					"--with-umem=%s" % ("yes" if self.options.umem else "no"),
					"--with-autotrace=%s" % ("yes" if self.options.autotrace else "no"),
					"--with-gslib=%s" % ("yes" if self.options.gslib else "no"),
					"--with-gvc=%s" % ("yes" if self.options.gvc else "no"),
					"--with-rsvg=%s" % ("yes" if self.options.rsvg else "no"),
					"--with-wmf=%s" % ("yes" if self.options.wmf else "no"),
					"--with-jpeg=%s" % ("yes" if self.options.jpeg else "no"),
					"--with-png=%s" % ("yes" if self.options.png else "no"),
					"--with-xml=%s" % ("yes" if self.options.xml else "no"),
					"--with-zlib=%s" % ("yes" if self.options.zlib else "no"),
					"--with-lzma=%s" % ("yes" if self.options.lzma else "no"),
					"--with-tiff=%s" % ("yes" if self.options.tiff else "no")
				]
				
				autotools.configure(configure_dir=self.source_subfolder, args=args)
				autotools.make()
				autotools.install()


	def package(self):
		if self.settings.os == "Windows":
			self.copy("*.h", dst="include/ImageMagick-7/MagickCore", src=os.path.join(self.source_subfolder, "MagickCore"))
			self.copy("*.h", dst="include/ImageMagick-7/MagickWand", src=os.path.join(self.source_subfolder, "MagickWand"))
			self.copy("*.h", dst="include/ImageMagick-7", src=os.path.join(self.source_subfolder, "Magick++", "lib"))
			self.copy("*Magick*.lib", dst="lib", keep_path=False)
			self.copy("*Magick*.dll", dst="bin", keep_path=False)
			self.copy("*Magick*.pdb", dst="bin", keep_path=False)


	def package_info(self):
		quantumDepth = str(getattr(self.options, "quantum-depth"))
		self.cpp_info.libs = [
			"MagickCore-7.Q%s" % quantumDepth,
			"MagickWand-7.Q%s" % quantumDepth,
			"Magick++-7.Q%s" % quantumDepth
		]
		self.cpp_info.includedirs = [
			"include",
			"include/ImageMagick-7"
		]
