%define name f2c
%define version 20001107
%define release %mkrel 8

Summary: The f2c Fortran to C/C++ conversion program and static libraries
Name: %{name}
Version: %{version}
Release: %{release}
License: Distributable
Group: Development/Other
Source: f2c-20001107.tar.bz2
Patch0: f2c-19991109.patch.bz2
URL: ftp://ftp.netlib.org/f2c/

%description
F2c converts Fortran 77 source code to C or C++ source files. If no
Fortran files are named on the command line, f2c can read Fortran from
standard input and write C to standard output.

F2c can also be used (with the -P option) to generate ANSI C header
files for calling Fortran routines from C.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q

%patch0 -p1  -b .tim

%build
%ifarch axp
MFLAG=-mieee
%endif

mkdir -p $RPM_BUILD_DIR/f2c-%{version}/libf2c/PIC

cp libf2c/makefile.u libf2c/Makefile
make -C src RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fPIC" MFLAG="$MFLAG" f2c
make -C libf2c RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fPIC" MFLAG="$MFLAG" 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir} $RPM_BUILD_ROOT/%{_mandir}/man1 $RPM_BUILD_ROOT/%{_libdir} $RPM_BUILD_ROOT/%{_includedir} 
install -m 644 libf2c/libf2c.a $RPM_BUILD_ROOT/%{_libdir}
install -m 644 f2c.h $RPM_BUILD_ROOT/%{_includedir}
install -s -m 755 src/f2c $RPM_BUILD_ROOT/%{_bindir}
install -s -m 755 fc $RPM_BUILD_ROOT/%{_bindir}
install -m 644 src/f2c.1t $RPM_BUILD_ROOT/%{_mandir}/man1/f2c.1
install -m 755 libf2c/libf2c.so.0.22 $RPM_BUILD_ROOT/%{_libdir}
ln -sf %{_libdir}/libf2c.so.0.22 $RPM_BUILD_ROOT/%{_libdir}libf2c.so

rm -rf $RPM_BUILD_ROOT/%_prefix/lib*libf2c.so
 
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc f2c.ps readme permission disclaimer changes src/Notice src/README
%{_libdir}/*
%{_includedir}/*
%{_bindir}/*
%{_mandir}/*/*

%clean
rm -rf $RPM_BUILD_ROOT
