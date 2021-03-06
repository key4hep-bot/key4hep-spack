
from spack import *
from spack.pkg.k4.Ilcsoftpackage import Key4hepPackage, k4_add_latest_commit_as_version 

class Fccdetectors(CMakePackage, Key4hepPackage):
    """Software framework of the FCC project"""
    homepage = "https://github.com/HEP-FCC/fccDetectors/"
    url      = "https://github.com/HEP-FCC/fccDetectors/archive/v0.16.tar.gz"
    git      = "https://github.com/HEP-FCC/fccDetectors.git"

    maintainers = ['vvolkl']

    version('main', branch='main')
    # can be removed once the ci is fixed
    version('master', branch='main')
    version("0.1pre03", tag="v0.1pre03")
    version("0.1pre01", tag="v0.1pre01")

    variant('framework', default=True, description="Build framework components")

    variant('cxxstd',
            default='17',
            values=('14', '17', '20'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('dd4hep +geant4')
    depends_on('edm4hep', when='+framework')
    depends_on('k4fwcore', when='+framework')

    def cmake_args(self):
        args = []
        # C++ Standard
        args.append('-DCMAKE_CXX_STANDARD=%s' % self.spec.variants['cxxstd'].value)
        return args

    def setup_run_environment(self, spack_env):
        spack_env.set("FCCDETECTORS", self.prefix.share.FCCDetectors)

    def test(self):
        self.run_test('geoDisplay', options=["$FCCDETECTORS/Detector/DetFCChhBaseline1/compact/FCChh_DectMaster.xml"], purpose="Construct FCChh Detector Geometry.")
