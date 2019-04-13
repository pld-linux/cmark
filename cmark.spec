#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	CommonMark parsing and rendering program
Name:		cmark
Version:	0.29.0
Release:	1
License:	BSD and MIT
Group:		Applications/Text
Source0:	https://github.com/CommonMark/cmark/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3bde2e450f46d3eb1494e2e6e8305d65
URL:		https://github.com/CommonMark/cmark
BuildRequires:	cmake
Requires:	%{name}-lib = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cmark is the C reference implementation of CommonMark, a rationalized
version of Markdown syntax with a spec.

%package lib
Summary:	CommonMark parsing and rendering library
Group:		Libraries

%description lib
Cmark is the C reference implementation of CommonMark, a rationalized
version of Markdown syntax with a spec.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name}-lib = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q

%build
mkdir build
cd build
%{cmake} \
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cmark
%{_mandir}/man1/cmark.1*

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcmark.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc README.md changelog.txt
%attr(755,root,root) %{_libdir}/libcmark.so
%{_includedir}/cmark*.h
%{_pkgconfigdir}/libcmark.pc
%{_libdir}/cmake/cmark-pld.cmake
%{_libdir}/cmake/cmark.cmake
%{_mandir}/man3/cmark.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcmark.a
%endif
