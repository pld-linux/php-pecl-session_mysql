%define		modname	session_mysql
Summary:	MySQL session save handler for PHP
Summary(pl.UTF-8):	Obsługa zapisywania sesji w bazie MySQL dla PHP
Name:		php-pecl-%{modname}
Version:	1.10
Release:	9
License:	MIT
Group:		Development/Languages/PHP
Source0:	http://websupport.sk/~stanojr/projects/session_mysql/%{modname}-%{version}.tgz
# Source0-md5:	66e933c506577ad43a0effbd2bbad715
Source1:	%{name}.ini
Source2:	%{name}.sql
URL:		http://websupport.sk/~stanojr/projects/session_mysql/
BuildRequires:	mysql-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Requires:	php-session
Provides:	php(session_mysql)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MySQL session save handler for PHP.

%description -l pl.UTF-8
Obsługa zapisywania sesji w bazie MySQL dla PHP.

%prep
%setup -q -n %{modname}-%{version}
cp -p %{SOURCE2} database.sql

%build
[ config.m4 -ot configure ] || rm -f configure
[ -f configure ] || phpize
[ configure -ot Makefile ] || rm -f Makefile
if [ ! -f Makefile ]; then
	%configure \
	--with-mysql=/usr
fi
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc LICENCE README database.sql
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
