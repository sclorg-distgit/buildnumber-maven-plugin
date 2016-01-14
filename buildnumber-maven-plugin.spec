%global pkg_name buildnumber-maven-plugin
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.2
Release:        7.10%{?dist}
Summary:        Build Number Maven Plugin

License:        MIT and ASL 2.0
URL:            http://svn.codehaus.org/mojo/tags/buildnumber-maven-plugin-1.2

# svn export http://svn.codehaus.org/mojo/tags/buildnumber-maven-plugin-1.2 buildnumber-maven-plugin
# tar caf buildnumber-maven-plugin-1.2.tar.xz buildnumber-maven-plugin
Source0:        buildnumber-maven-plugin-1.2.tar.xz
Source2:        http://www.apache.org/licenses/LICENSE-2.0.txt

BuildArch: 	noarch

# Basic stuff
BuildRequires: %{?scl_prefix_java_common}javapackages-tools

# Maven and its dependencies
BuildRequires: %{?scl_prefix_java_common}maven-local
BuildRequires: %{?scl_prefix}maven-plugin-plugin
BuildRequires: %{?scl_prefix}maven-resources-plugin
BuildRequires: %{?scl_prefix}maven-compiler-plugin
BuildRequires: %{?scl_prefix}maven-install-plugin
BuildRequires: %{?scl_prefix}maven-javadoc-plugin
BuildRequires: %{?scl_prefix}maven-jar-plugin
BuildRequires: %{?scl_prefix}maven-enforcer-plugin
BuildRequires: %{?scl_prefix}maven-invoker-plugin
BuildRequires: %{?scl_prefix}maven-surefire-provider-junit
BuildRequires: %{?scl_prefix}maven-surefire-plugin
BuildRequires: %{?scl_prefix}plexus-containers-component-javadoc
BuildRequires: %{?scl_prefix}plexus-containers-container-default
BuildRequires: %{?scl_prefix}plexus-utils
BuildRequires: %{?scl_prefix}jna
BuildRequires: %{?scl_prefix}mojo-parent
BuildRequires: %{?scl_prefix}maven-project
BuildRequires: %{?scl_prefix}maven-scm


%description
This mojo is designed to get a unique build number for each time you build
your project. So while your version may remain constant at 1.0-SNAPSHOT
for many iterations until release, you will have a build number that can
uniquely identify each build during that time. The build number is obtained
from scm, and in particular, at this time, from svn. You can then place that
build number in metadata, which can be accessed from your app, if desired.

The mojo also has a couple of extra functions to ensure you get the proper
build number. First, your local repository is checked to make sure it is
up to date. Second, your local repository is automatically updated, so that
you get the latest build number. Both these functions can be suppressed,
if desired.

Optionally, you can configure this mojo to produce a revision based on a
timestamp, or on a sequence, without requiring any interaction with an
SCM system. Note that currently, the only supported SCM is subversion.


%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
cp -p %{SOURCE2} .

%pom_remove_dep com.google.code.maven-scm-provider-svnjava:maven-scm-provider-svnjava
%pom_remove_dep org.tmatesoft.svnkit:svnkit
# needed by svnkit - and we build the package without it
%pom_remove_dep net.java.dev.jna:jna

%mvn_file : %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# tests skipped due to invoker problems with local repository tests
%mvn_build -f -- -Dmaven.compile.target=1.5
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE.txt LICENSE-2.0.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt LICENSE-2.0.txt

%changelog
* Wed Jun 10 2015 Michal Srb <msrb@redhat.com> - 1.2-7.10
- Remove dep on jna

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.2-7.9
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1.2-7.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-7.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-7.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-7.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-7.4
- Remove requires on java

* Fri Feb 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-7.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-7.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-7.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.2-7
- Mass rebuild 2013-12-27

* Fri Aug 23 2013 Michal Srb <msrb@redhat.com> - 1.2-6
- Migrate away from mvn-rpmbuild (Resolves: #997488)
- Remove unneeded BR

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-5
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-4
- Remove unneeded BR: maven-idea-plugin

* Thu Feb 28 2013 Weinan Li <weli@redhat.com> - 1.2-3
- remove unnecessary maven-doxia dependencies

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.2-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan 29 2013 David Xie <david.scriptfan@gmail.com> - 1.2-1
- Upgrade to 1.2

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-2
- Install ASL 2.0 license
- Remove rpm bug workaround

* Wed Jul 25 2012 Tomas Radej <tradej@redhat.com> - 1.1-1
- Updated to latest upstream version
- Replaced patches with pom macros

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-5
- Remove dependency on svnkit

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 30 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-3
- Add missing (Build)Requires
- Use new add_maven_depmap macro

* Wed Jun 8 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-2
- Do not require maven2.
- Guidelines fixes.

* Mon Apr 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-1
- Update to latest upstream
- Build with maven 3
- Tweaks according to new guidelines
- Versionless jars & javadocs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.11.b4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 11 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-0.10.b4
- Added mojo-parent to BR/R

* Wed Sep 1 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.9.b4
- Fix build and use new maven plugins names.

* Thu Jun 17 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.8.b4
- BR maven2-common-poms.

* Thu Jun 17 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.7.b4
- Disable it-tests and changes plugin.

* Thu Jun 17 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.6.b4
- Skip tests to be able to rebuild.

* Thu Jun 17 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.5.b4
- Add missing requires.

* Thu May 27 2010 Weinan Li <weli@redhat.com> - 1.0-0.4.b4
- License.txt and Readme.txt added as %doc

* Thu May 27 2010 Weinan Li <weli@redhat.com> - 1.0-0.3.b4
- Fix javadoc dangling-relative-symlink

* Wed May 26 2010 Weinan Li <weli@redhat.com> - 1.0-0.2.b4
- Add requires on jpackage-utils for javadoc subpackage
- Add standard jpackage-utils requires on main package
- Use global instead of define
- Fix license to MIT
- fix incoherent-version-in-changelog

* Mon May 24 2010 Weinan Li <weli@redhat.com> - 1.0-0.1.b4
- Initial package
