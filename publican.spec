# TODO:
# - common-web
# - fix tests (currently they require wkhtmltopdf built with patched qt)
#
# Conditional build:
%bcond_with	tests	# do perform "./Build test"

%include	/usr/lib/rpm/macros.perl
Summary:	Publishing tool based on DocBook XML
Summary(pl.UTF-8):	Narzędzie do publikowania, oparte na formacie Docbook XML
Name:		publican
Version:	4.3.0
Release:	1
License:	CC0 (Common Content files), GPL v2+ or Artistic v1.0 (the rest)
Group:		Applications/Publishing/XML
Source0:	https://fedorahosted.org/releases/p/u/publican/Publican-v%{version}.tar.gz
# Source0-md5:	95564b6559661c7c7266f17f0502ae31
Patch0:		%{name}-test.patch
URL:		https://fedorahosted.org/publican/
BuildRequires:	perl-Archive-Tar >= 1.84
BuildRequires:	perl-Archive-Zip
BuildRequires:	perl-Config-Simple
BuildRequires:	perl-DBI
BuildRequires:	perl-DateTime
BuildRequires:	perl-DateTime-Format-DateParse
BuildRequires:	perl-Devel-Cover
BuildRequires:	perl-Encode
BuildRequires:	perl-File-Copy-Recursive >= 0.38
BuildRequires:	perl-File-Find-Rule
BuildRequires:	perl-File-Inplace
BuildRequires:	perl-File-Slurp
BuildRequires:	perl-File-Which
BuildRequires:	perl-File-pushd
BuildRequires:	perl-HTML-Format
BuildRequires:	perl-HTML-FormatText-WithLinks
BuildRequires:	perl-HTML-FormatText-WithLinks-AndTables >= 0.02
BuildRequires:	perl-HTML-Tree
BuildRequires:	perl-HTML-WikiConverter
BuildRequires:	perl-HTML-WikiConverter-Markdown >= 0.06
BuildRequires:	perl-I18N-LangTags
BuildRequires:	perl-IO-String
BuildRequires:	perl-Lingua-EN-Fathom
BuildRequires:	perl-List-MoreUtils
BuildRequires:	perl-Locale-Maketext-Gettext
BuildRequires:	perl-Locale-Maketext-Lexicon
BuildRequires:	perl-Locale-Msgfmt
BuildRequires:	perl-Locale-PO >= 0.24
BuildRequires:	perl-Makefile-Parser
BuildRequires:	perl-Module-Build
BuildRequires:	perl-Sort-Versions
BuildRequires:	perl-String-Similarity
BuildRequires:	perl-Syntax-Highlight-Engine-Kate >= 0.09
BuildRequires:	perl-Template-Toolkit
BuildRequires:	perl-Term-ANSIColor
BuildRequires:	perl-Text-CSV_XS
BuildRequires:	perl-XML-LibXML >= 1.70
BuildRequires:	perl-XML-LibXSLT >= 1.70
BuildRequires:	perl-XML-Simple
BuildRequires:	perl-XML-TreeBuilder >= 5.4
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	perl-version >= 0.77
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	docbook-style-xsl >= 1.76.1
BuildRequires:	perl-Test-Pod >= 1.14
BuildRequires:	perl-Test-Pod-Coverage >= 1.04
BuildRequires:	perl-Test-Simple
# because of WEB_TEMPLATE_PATH in publican script
BuildRequires:	publican >= 3.1
BuildRequires:	wkhtmltopdf
%endif
Requires:	docbook-style-xsl >= 1.76.1
Requires:	perl-Archive-Tar >= 1.84
Requires:	perl-File-Copy-Recursive >= 0.38
Requires:	perl-HTML-FormatText-WithLinks-AndTables >= 0.02
Requires:	perl-HTML-WikiConverter-Markdown >= 0.06
Requires:	perl-Locale-PO >= 0.24
Requires:	perl-Syntax-Highlight-Engine-Kate >= 0.09
Requires:	perl-XML-LibXML >= 1.70
Requires:	perl-XML-LibXSLT >= 1.70
Requires:	perl-XML-TreeBuilder >= 5.4
Requires:	perl-version >= 0.77
Requires:	wkhtmltopdf
# to produce RPMs
Suggests:	rpm-build
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# FIXME
%define		wwwdir		%{_datadir}/html/docs

%description
Publican is a DocBook publication system, not just a DocBook
processing tool. As well as ensuring your DocBook XML is valid,
Publican works to ensure your XML is up to publishable standard.

%description -l pl.UTF-8
Publican to docbookowy system publikacji, nie będący tylko narzędziem
do przetwarzania DocBooka. Poza sprawdzeniem, że DocBook XML jest
poprawny, Publican sprawdza, czy XML jest zgodny z aktualnym
standardem publikacji.

%package doc
Summary:	Documentation for the Publican package
Summary(pl.UTF-8):	Dokumentacja do pakietu Publican
License:	FDL
Group:		Documentation

%description doc
Publican is a tool for publishing material authored in DocBook XML.
This guide explains how to create and build books and articles using
Publican. It is not a DocBook XML tutorial and concentrates solely on
using the Publican tools.

%description doc -l pl.UTF-8
Publican to narzędzie do tworzenia publikacji z materiałów pisanych w
formacie DocBook XML. Ten podręcznik opisuje tworzenie książek oraz
artykułów przy użyciu pakietu Publican. Nie jest to podręcznik do
DocBook XML-a i skupia się wyłącznie na użyciu narzędzi z pakietu
Publican.

%package common-web
Summary:        Website style for common brand
Summary(pl.UTF-8):	Styl strony WWW dla ogólnego szablonu
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description common-web
Website style for common brand.

%description common-web -l pl.UTF-8
Styl strony WWW dla ogólnego szablonu.

%package -n bash-completion-publican
Summary:	bash-completion for Publican
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów dla programu Publican
Group:		Applications/Shells
Requires:	bash-completion

%description -n bash-completion-publican
bash-completion for Publican.

%description -n bash-completion-publican -l pl.UTF-8
Bashowe uzupełnianie parametrów dla programu Publican.

%prep
%setup -q -n Publican-v%{version}
%patch0 -p1

# just a copy of de_CH
%{__rm} po/de-CH.po

%build
%{__perl} Build.PL \
	--nocolours=1 \
	perl=%{__perl} \
	installdirs=vendor
./Build

%{?with_tests:./Build test}

# publish Users_Guide
dir=$(pwd)
cd Users_Guide
%{__perl} -CDAS -I $dir/blib/lib $dir/blib/script/publican build \
	--formats=html-desktop \
	--publish \
	--langs=all \
	--common_config="$dir/blib/datadir" \
	--common_content="$dir/blib/datadir/Common_Content" \
	--nocolours

%install
rm -rf $RPM_BUILD_ROOT

./Build install \
	destdir=$RPM_BUILD_ROOT

for f in po/*.po ; do
	lang=$(basename "$f" .po)
	install -d $RPM_BUILD_ROOT%{_datadir}/locale/$lang/LC_MESSAGES
	msgfmt -c -v -o $RPM_BUILD_ROOT%{_datadir}/locale/$lang/LC_MESSAGES/publican.mo "$f"
done

%if 0
install -d $RPM_BUILD_ROOT%{wwwdir}/common
dir=$(pwd)
cd datadir/Common_Content/common
%{__perl} -CA -I $dir/blib/lib $dir/blib/script/publican install_brand --web --path=$RPM_BUILD_ROOT%{wwwdir}/common
%endif

%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{sr@Latn,sr@latin}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CC0 Changes LICENSE README TODO
%attr(755,root,root) %{_bindir}/db4-2-db5
%attr(755,root,root) %{_bindir}/db5-valid
%attr(755,root,root) %{_bindir}/publican
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/publican-website.cfg
%{perl_vendorlib}/Publican.pm
%{perl_vendorlib}/Publican
%{_datadir}/publican
%{_mandir}/man1/publican.1p*
%{_mandir}/man3/Publican*.3pm*

%files doc
%defattr(644,root,root,755)
%doc Users_Guide/publish/desktop/*

%files -n bash-completion-publican
%defattr(644,root,root,755)
/etc/bash_completion.d/_publican
