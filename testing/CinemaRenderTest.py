import pytest
import pytest_xvfb

import pycinema

@pytest.fixture(autouse=True, scope='session')
def ensure_xvfb():
    if not pytest_xvfb.xvfb_available():
        raise Exception("Tests need Xvfb to run.")

def test_render():

    resolution = (512,256)
    phiSamples = (20,360,60)
    thetaSamples = (20,20,45)
    time = 0.1

    planeImages = pycinema.DemoCDB()
    planeImages.inputs.Objects.set((1,0,0),False) # Plane Only
    planeImages.inputs.Resolution.set(resolution,False)
    planeImages.inputs.PhiSamples.set(phiSamples,False)
    planeImages.inputs.ThetaSamples.set(thetaSamples,False)
    planeImages.inputs.Time.set(time,False)
    planeImages.update()

    sphereImages = pycinema.DemoCDB()
    sphereImages.inputs.Objects.set((0,1,1),False) # Big and Small Sphere
    sphereImages.inputs.Resolution.set(resolution,False)
    sphereImages.inputs.PhiSamples.set(phiSamples,False)
    sphereImages.inputs.ThetaSamples.set(thetaSamples,False)
    sphereImages.inputs.Time.set(time,False)
    sphereImages.update()

    spheresColordByY = pycinema.ColorMapping()
    spheresColordByY.inputs.Channel.set( "Y", False )
    spheresColordByY.inputs.Map.set( "plasma", False )
    spheresColordByY.inputs.Range.set( (0,2), False )
    spheresColordByY.inputs.Images.set( sphereImages.outputs.Images )

    depthCompositing = pycinema.DepthCompositing()
    depthCompositing.inputs.ImagesA.set(planeImages.outputs.Images, False )
    depthCompositing.inputs.ImagesB.set(spheresColordByY.outputs.Images, False )
    depthCompositing.update()

    ssao = pycinema.ShaderSSAO()
    ssao.inputs.Radius.set( 0.1, False )
    ssao.inputs.Samples.set( 256, False )
    ssao.inputs.Diff.set( 0.5, False )
    ssao.inputs.Images.set( depthCompositing.outputs.Images )

    annotation = pycinema.Annotation()
    annotation.inputs.Color.set( (255,255,255), False )
    annotation.inputs.Size.set( 10, False )
    annotation.inputs.XY.set( (0,0), False )
    annotation.inputs.Spacing.set( 20, False )
    annotation.inputs.Images.set( ssao.outputs.Images )

    # Test Output
    GT = [['142.5', '0.0', '255.0', '0.189', '0.408'], ['142.5', '0.0', '255.0', '0.189', '0.408'], ['142.4', '0.0', '255.0', '0.189', '0.408'], ['142.6', '0.0', '255.0', '0.189', '0.408'], ['142.5', '0.0', '255.0', '0.189', '0.408'], ['142.4', '0.0', '255.0', '0.189', '0.408']]
    images = annotation.outputs.Images.get();
    s = []
    for i in range(len(images)):
        image = images[i]
    #     import PIL
    #     display(PIL.Image.fromarray(image.channel['RGBA']))
        data = [
            "{:.1f}".format(image.channel['RGBA'].mean()),
            "{:.1f}".format(image.channel['RGBA'].min()),
            "{:.1f}".format(image.channel['RGBA'].max()),
            "{:.3f}".format(image.channel['Depth'].min()),
            "{:.3f}".format(image.channel['Depth'].max())
        ]
        s.append(data)
        if s[i] != GT[i]:
            print(str(data))
            print(GT[i])
            raise ValueError('Generated Data does not correspond to Ground Truth')
    # print(s)
    print("Test Complete")











