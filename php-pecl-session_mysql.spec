# on apache2 restart when module can't connect to database issues errors that can't be understand why:
# [error] [client ::1] PHP Fatal error:  session_start(): Failed to initialize storage module: mysql (path: /var/run/php) in class.auth.php on line 22
# [error] [client x.x.x.x] PHP Fatal error:  session_start(): Failed to initialize storage module: mysql (path: /var/run/php) in class.auth.php on line 22
#
%define		_modname	session_mysql
Summary:	MySQL session save handler for PHP
Summary(pl.UTF-8):	Obsługa zapisywania sesji w bazie MySQL dla PHP
Name:		php-pecl-%{_modname}
Version:	1.9
Release:	1
License:	MIT
Group:		Development/Languages/PHP
Source0:	http://websupport.sk/~stanojr/projects/session_mysql/%{_modname}-%{version}.tgz
# Source0-md5:	0eea3ce6c97ac5a2fdce71f23ce1ff2b
Source1:	%{name}.ini
Source2:	%{name}.sql
Patch0:		%{name}-leak.patch
URL:		http://websupport.sk/~stanojr/projects/session_mysql/
BuildRequires:	mysql-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Provides:	php(session_mysql)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MySQL session save handler for PHP.
- supports locking
- very quiet (doesn't log any error) (but upper session functions can
  print some error).

%description -l pl.UTF-8
Obsługa zapisywania sesji w bazie MySQL dla PHP.
- obsługuje blokowanie
- bardzo cicha (sama nie loguje żadnych błędów; ale funkcje wyższego
  poziomu mogą wypisywać błędy).

%prep
%setup -q -n %{_modname}-%{version}
%patch0 -p1
cp -a %{SOURCE2} database.sql

%build
phpize
%configure \
	--with-mysql=/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
install %{SOURCE1} $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini

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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
