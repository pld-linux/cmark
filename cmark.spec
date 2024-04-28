#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	CommonMark parsing and rendering program
Summary(pl.UTF-8):	Program do analizy i renderowania formatowania CommonMark
Name:		cmark
Version:	0.31.0
Release:	1
License:	BSD and MIT
Group:		Applications/Text
#Source0Download: https://github.com/CommonMark/cmark/releases
Source0:	https://github.com/CommonMark/cmark/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0f18ad50f77cc20e048316857f187da2
URL:		https://github.com/CommonMark/cmark
BuildRequires:	cmake >= 3.7
Requires:	%{name}-lib = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cmark is the C reference implementation of CommonMark, a rationalized
version of Markdown syntax with a spec.

%description -l pl.UTF-8
CMark to wzorcowa implementacja w C formatu CommonMark -
zracjonalizowanej wersji składni Markdown, posiadającej specyfikację.

%package lib
Summary:	CommonMark parsing and rendering library
Summary(pl.UTF-8):	Biblioteka do analizy i renderowania formatowania CommonMark
Group:		Libraries

%description lib
Cmark is the C reference implementation of CommonMark, a rationalized
version of Markdown syntax with a spec.

%description lib -l pl.UTF-8
CMark to wzorcowa implementacja w C formatu CommonMark -
zracjonalizowanej wersji składni Markdown, posiadającej specyfikację.

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
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF

%{__make}
cd ..
%endif

install -d build
cd build
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT

# ensure executable comes from shared build
%{__rm} $RPM_BUILD_ROOT%{_bindir}/cmark
%endif

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
%doc COPYING README.md changelog.txt
%attr(755,root,root) %{_libdir}/libcmark.so.%{version}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcmark.so
%{_includedir}/cmark*.h
%{_pkgconfigdir}/libcmark.pc
%{_libdir}/cmake/cmark
%{_mandir}/man3/cmark.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcmark.a
%endif
