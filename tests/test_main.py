import shotgun_query_field_test.main
import shotgun_api3

def test_sg_instance_created():
    sg = shotgun_query_field_test.main.get_shotgun_instance()
    assert isinstance(sg, shotgun_api3.Shotgun)
