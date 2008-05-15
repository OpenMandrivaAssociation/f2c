%define major		0
%define libname		%mklibname %name %major
%define develname	%mklibname %name -d

Summary:	Fortran to C/C++ converter
Name:		f2c
Version:	20080407
Release:	%{mkrel 1}
License:	MIT
Group:		Development/Other
# Create directory named %{name}-%{version}. Download all files from
# the URL below except libf2c.zip into it. Don't get the msdos or
# mswin directories, do get the src directory. Download libf2c.zip
# directly and use it as Source1. - AdamW 2008/05
Source0:	f2c-%{version}.tar.lzma
Source1:	ftp://ftp.netlib.org/f2c/libf2c.zip
Patch0:		f2c-20080407.patch
URL:		ftp://ftp.netlib.org/f2c/
Buildroot:	%{_tmppath}/%{name}-buildroot
# You need the library and devel package to actually build any code
# produced by f2c, so let's suggest it - AdamW 2008/05
Suggests:	%{develname}

%description
F2c converts Fortran 77 source code to C or C++ source files. If no
Fortran files are named on the command line, f2c can read Fortran from
standard input and write C to standard output.

F2c can also be used (with the -P option) to generate ANSI C header
files for calling Fortran routines from C.

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{name} < 20080407

%description -n %{libname}
F2c converts Fortran 77 source code to C or C++ source files. If no
Fortran files are named on the command line, f2c can read Fortran from
standard input and write C to standard output.

F2c can also be used (with the -P option) to generate ANSI C header
files for calling Fortran routines from C.

%package -n %{develname}
Summary:	Development headers for %{name}
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Conflicts:	%{name} < 20080407

%description -n %{develname}
F2c converts Fortran 77 source code to C or C++ source files. If no
Fortran files are named on the command line, f2c can read Fortran from
standard input and write C to standard output.

F2c can also be used (with the -P option) to generate ANSI C header
files for calling Fortran routines from C.

%prep
rm -rf %{buildroot}
%setup -q
mkdir libf2c
pushd libf2c
unzip %{SOURCE1}
popd
make -C src -f makefile.u xsum.out
%patch0 -p1  -b .tim

%build
%ifarch axp
MFLAG=-mieee
%endif

mkdir -p libf2c/PIC

cp libf2c/makefile.u libf2c/Makefile
cp src/makefile.u src/Makefile
RPM_OPT_FLAGS="%{optflags} -fPIC" make -C src
RPM_OPT_FLAGS="%{optflags} -fPIC" make -C libf2c

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_mandir}/man1 %{buildroot}%{_libdir} %{buildroot}%{_includedir} 
install -m 644 libf2c/libf2c.a %{buildroot}%{_libdir}
install -m 644 f2c.h %{buildroot}%{_includedir}
install -s -m 755 src/f2c %{buildroot}%{_bindir}
install -m 755 fc %{buildroot}%{_bindir}
install -m 644 src/f2c.1t %{buildroot}%{_mandir}/man1/f2c.1
install -m 755 libf2c/libf2c.so.0.22 %{buildroot}%{_libdir}
ln -sf %{_libdir}/libf2c.so.0.22 %{buildroot}%{_libdir}/libf2c.so
 
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc f2c.ps readme permission disclaimer changes src/Notice

%{_bindir}/*
%{_mandir}/*/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.*a

%clean
rm -rf %{buildroot}
