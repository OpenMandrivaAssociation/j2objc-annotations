Name:		j2objc-annotations
Version:	3.1
Release:	1
Summary:	Annotations used by the J2ObjC translator
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/google/j2objc
# Annotations module of tag 3.1. The rest of that tag is the Objective-C
# translator, which this package does not build.
Source0:	https://github.com/google/j2objc/archive/refs/tags/3.1.tar.gz#/j2objc-annotations-3.1.tar.gz

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	sysjar

%description
Annotations that tell the J2ObjC translator how to translate Java.
Guava 33.6.0 marks reflection and weak references with this API.
The tag POM says 3.1-SNAPSHOT; the published coordinate is 3.1.

%prep
%autosetup -n j2objc-annotations-%{version} -p1
find . \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -delete
sed -i 's|>3.1-SNAPSHOT<|>3.1<|' pom.xml
grep -q '<version>3.1</version>' pom.xml

%build
mkdir -p classes
find src/main/java -name '*.java' ! -name module-info.java > sources.list
test "$(wc -l < sources.list)" -eq 20
javac --release 8 -encoding UTF-8 -d classes @sources.list
jar cf j2objc-annotations.jar -C classes .

%install
sysjar install --buildroot %{buildroot} \
	--artifact pom.xml:j2objc-annotations.jar \
	--file-name j2objc-annotations \
	--filelist .mfiles

%check
mkdir -p check
cat > check/Smoke.java <<'END'
import com.google.j2objc.annotations.ReflectionSupport;
public class Smoke {
	public static void main(String[] args) {
		System.out.println("j2objc_ok " + ReflectionSupport.Level.FULL.name());
	}
}
END
JAR=%{buildroot}%{_javadir}/j2objc-annotations.jar
test -f "$JAR"
javac --release 8 -encoding UTF-8 -cp "$JAR" -d check check/Smoke.java
java -cp "check:$JAR" Smoke > check/out.txt
cat check/out.txt
grep -F -q 'j2objc_ok FULL' check/out.txt

%files -f .mfiles
%doc LICENSE
