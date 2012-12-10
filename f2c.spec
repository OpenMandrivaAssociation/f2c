Summary: The f2c Fortran to C/C++ conversion program and static libraries.
Name: f2c
Version: 20031026
Release: 3.0.1%{?dist}
License: Distributable
Group: Development/Languages
Source: f2c.tar
Patch0: f2c-20031026.patch 
URL: http://netlib.org/f2c/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: unzip
Obsoletes: f2c-libs

%description
F2c converts Fortran 77 source code to C or C++ source files. If no
Fortran files are named on the command line, f2c can read Fortran from
standard input and write C to standard output.


%prep
%setup -q -n %{name}
unzip libf2c.zip
%patch0 -p1  -b .tim

%build
%ifarch axp
MFLAG=-mieee
%endif

mkdir -p $RPM_BUILD_DIR/f2c-%{version}/libf2c/PIC

cp src/makefile.u src/Makefile
cp libf2c/makefile.u libf2c/Makefile
make -C src RPM_OPT_FLAGS="$RPM_OPT_FLAGS" MFLAG="$MFLAG" f2c
make -C libf2c RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fPIC" MFLAG="$MFLAG" 

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/%{_mandir}/man1
install -m 644 libf2c/libf2c.a %{buildroot}%{_libdir}
install -m 644 f2c.h %{buildroot}%{_includedir}
install -s -m 755 src/f2c %{buildroot}%{_bindir}/f2c
install -m 644 src/f2c.1t %{buildroot}/%{_mandir}/man1/f2c.1
install -m 755 libf2c/libf2c.so.0.22 %{buildroot}%{_libdir}
ln -sf libf2c.so.0.22 %{buildroot}%{_libdir}/libf2c.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc f2c.ps readme permission disclaimer changes src/Notice src/README
%{_bindir}/*
%{_libdir}/libf2c.so.*
%{_mandir}/man1/f2c.1*
%{_includedir}/*
%{_libdir}/libf2c.a
%{_libdir}/libf2c.so

%clean
rm -rf %{buildroot}

%changelog
* Sat Jun 14 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 20031026-3.0.1
- Fix not utf-8 specfile entries.

* Wed Jul 16 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Updated to 20030320, adapted the patch.

* Thu Jan 11 2001 Trond Eivind Glomsrød <teg@redhat.com>
- add -fPIC to the CFLAGS

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Thu Jun 22 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath} and %%{_mandir}

* Wed May 10 2000 Tim Powers <timp@redhat.com>
- updated to 20000510

* Fri Feb 04 2000 Tim Powers <timp@redhat.com>
- fixed so that man pages are gzip'ed

* Tue Nov 9 1999 Tim Powers <timp@redhat.com>
- updated source to 19991109
- quiet setup

* Wed Jul 28 1999 Tim Powers <timp@redhat.com>
- updated source to 19990728
- updated patch
- added %defattr
- moved changleg to bottom of spec
- built for 6.1

* Tue Apr 27 1999 Bill Nottingham <notting@redhat.com>
- build for powertools

* Tue Mar 30 1999 Alexander L. Belikoff <abel@bfr.co.il>

- upgraded to version 19990326
- adjusted the types in f2c.h for the Alpha
- f2c source is packaged as a .tar.gz file and libf2c inside is already
  extracted - this makes building patches much easier.

* Thu May 07 1998 Prospector System <bugs@redhat.com>

- translations modified for de, fr, tr

* Wed Oct 29 1997 Cristian Gafton <gafton@redhat.com>
- upgraded to version 19970805
- added buildroot; removed libs subpackage and made it obsoleted

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Apr 17 1997 Erik Troan <ewt@redhat.com>
- Changed axp tag to alpha

* Fri Apr 11 1997 Michael Fulbright <msf@redhat.com>
- Fixed man page and made it install the troff version in correct place.
- Removed checksum calculation on sources, otherwise we cant patch source!
