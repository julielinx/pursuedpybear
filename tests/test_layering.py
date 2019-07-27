import ppb.camera as camera
import ppb.scenes as scenes


class LayeredSprite:

    def __init__(self, layer):
        self.layer = layer


class NoLayer:
    pass


def test_layering_attribute():

    class LayeredScene(scenes.BaseScene):

        def __init__(self):
            super().__init__()
            for x in range(5):
                self.add(LayeredSprite(x))

    scene = LayeredScene()
    for lower_sprite, higher_sprite in zip(scene.sprite_layers(), list(scene.sprite_layers())[1:]):
        if isinstance(lower_sprite, camera.Camera) or isinstance(higher_sprite, camera.Camera):
            continue
        assert lower_sprite.layer < higher_sprite.layer


def test_change_layer():

    test_sprite = LayeredSprite(0)
    ones = tuple(LayeredSprite(1) for _ in range(3))

    scene = scenes.BaseScene()
    scene.add(test_sprite)
    for sprite in ones:
        scene.add(sprite)

    assert list(scene.sprite_layers())[0] == test_sprite

    test_sprite.layer = 2

    assert list(scene.sprite_layers())[-1] == test_sprite


def test_layering_without_layer_attribute():

    test_sprite = NoLayer()
    scene = scenes.BaseScene()

    scene.add(test_sprite)
    for x in range(1, 6):
        scene.add(LayeredSprite(x))

    assert list(scene.sprite_layers())[0] == test_sprite


def test_set_default_layer():

    class DefaultLayer(scenes.BaseScene):
        default_layer = 3

    scene = DefaultLayer()

    scene.add(LayeredSprite(layer=1))
    scene.add(LayeredSprite(layer=5))
    test_sprite = NoLayer()
    scene.add(test_sprite)

    assert list(scene.sprite_layers)[1] is test_sprite
