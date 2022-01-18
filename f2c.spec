%define major      0
%define sover      %{major}.22
%define libf2cname %mklibname %{name} %{major}

Name:           f2c
Summary:        A Fortran 77 to C/C++ conversion program
Version:	20210928
Release:	1
License:        MIT
Group:          Development/C
URL:            http://www.netlib.org/f2c/
Source0:        http://www.netlib.org/f2c/src.tgz
Source1:        http://www.netlib.org/f2c/libf2c.zip
Source2:        http://www.netlib.org/f2c/f2c.pdf
Source3:        http://www.netlib.org/f2c/f2c.ps
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
Obsoletes:  %{_lib}f2c < 20110801-8

%description -n %{libf2cname}
Dynamic libraries from %{name}.

%prep
%setup -q -c %{name}-%{version}
mkdir lib%{name}
unzip -qq %{SOURCE1} -d lib%{name}
%patch0
%patch1
%patch2 -p1 -b .parallel-make

# Set library soversion
sed -i "s/@SOVER@/%{sover}/" lib%{name}/makefile.u

# PDF and PS documentation
cp %{SOURCE2} %{SOURCE3} .

%build
%make_build -C src -f makefile.u CFLAGS="%{optflags}" f2c CC=%{__cc}
%make_build -C libf2c -f makefile.u CFLAGS="%{optflags} -fPIC" CC=%{__cc}

%install
install -D -p -m 644 src/%{name}.h %{buildroot}%{_includedir}/%{name}.h
install -D -p -m 755 src/%{name} %{buildroot}%{_bindir}/%{name}
install -D -p -m 644 src/%{name}.1t %{buildroot}%{_mandir}/man1/%{name}.1
install -D -p -m 755 lib%{name}/lib%{name}.so.%{sover} %{buildroot}%{_libdir}/lib%{name}.so.%{sover}
ln -s lib%{name}.so.%{sover} %{buildroot}%{_libdir}/lib%{name}.so.0
ln -s lib%{name}.so.%{sover} %{buildroot}%{_libdir}/lib%{name}.so

%files
%doc %{name}.ps %{name}.pdf src/changes src/README
%license libf2c/Notice
%{_bindir}/%{name}
%{_mandir}/man1/*
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so

%files -n %{libf2cname}
%doc libf2c/README
%license libf2c/Notice
%{_libdir}/lib%{name}.so.%{major}{,.*}
