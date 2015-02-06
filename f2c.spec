%define major	0
%define libf2cname %mklibname f2c %{major}

Name:           f2c
Summary:        A Fortran 77 to C/C++ conversion program
Version:        20110801
Release:        4
License:        MIT
Group:          Development/C
URL:            http://netlib.org/f2c/
Source0:        ftp://netlib.org/f2c.tar
# Patch makefile to build a shared library
Patch0:		f2c-20090411.patch
Patch1:		f2c-arithchk.patch
Patch2:		f2c-parallel-make.patch
BuildRequires:  unzip
Requires:       %{libf2cname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description
F2c converts Fortran 77 source code to C or C++ source files. If no
Fortran files are named on the command line, f2c can read Fortran from
standard input and write C to standard output.

%package -n %{libf2cname}
Summary:    Dynamic libraries from %{name}
Group:      System/Libraries

%description -n %{libf2cname}
Dynamic libraries from %{name}.

%prep
%setup -q -n %{name}
mkdir lib%{name}
pushd lib%{name}
unzip ../lib%{name}.zip
popd
%patch0
%patch1
%patch2 -p1 -b .parallel-make

%build
cp src/makefile.u src/Makefile
cp lib%{name}/makefile.u lib%{name}/Makefile
%make -C src CFLAGS="%{optflags}" f2c
%make -C lib%{name} CFLAGS="%{optflags} -fPIC"

%install
rm -rf %{buildroot}
install -D -p -m 644 %{name}.h %{buildroot}%{_includedir}/%{name}.h
install -D -p -m 755 src/%{name} %{buildroot}%{_bindir}/%{name}
install -D -p -m 644 src/%{name}.1t %{buildroot}%{_mandir}/man1/%{name}.1
install -D -p -m 755 lib%{name}/lib%{name}.so.0.22 %{buildroot}%{_libdir}/lib%{name}.so.0.22
ln -s lib%{name}.so.0.22 %{buildroot}%{_libdir}/lib%{name}.so.0
ln -s lib%{name}.so.0.22 %{buildroot}%{_libdir}/lib%{name}.so

%files
%doc %{name}.ps %{name}.pdf readme changes src/README
%{_bindir}/%{name}
%{_mandir}/man1/*
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so

%files -n %{libf2cname}
%doc permission disclaimer src/Notice
%{_libdir}/lib%{name}.so.*
