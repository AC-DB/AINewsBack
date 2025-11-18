from ainewsback.utils.password import PasswordUtil


def test_generate_salt():
    """测试盐值生成"""
    salt1 = PasswordUtil.generate_salt()
    salt2 = PasswordUtil.generate_salt()

    assert len(salt1) == 32  # 16字节 = 32个十六进制字符
    assert salt1 != salt2  # 每次生成的盐值应该不同


def test_hash_password():
    """测试密码哈希"""
    password = "test123"
    salt = "abc123"

    hashed1 = PasswordUtil.hash_password(password, salt)
    hashed2 = PasswordUtil.hash_password(password, salt)

    assert hashed1 == hashed2  # 相同密码和盐值应产生相同哈希
    assert len(hashed1) == 64  # SHA-256 = 64个十六进制字符


def test_create_password():
    """测试创建密码"""
    password = "mypassword"
    hashed, salt = PasswordUtil.create_password(password)

    assert len(hashed) == 64
    assert len(salt) == 32


def test_verify_password():
    """测试密码验证"""
    password = "correct_password"
    hashed, salt = PasswordUtil.create_password(password)

    # 正确密码应验证通过
    assert PasswordUtil.verify_password(password, hashed, salt) is True

    # 错误密码应验证失败
    assert PasswordUtil.verify_password("wrong_password", hashed,
                                        salt) is False


def test_generate_random_password():
    """测试随机密码生成"""
    pwd1 = PasswordUtil.generate_random_password(10)
    pwd2 = PasswordUtil.generate_random_password(10)

    assert len(pwd1) == 10
    assert pwd1 != pwd2
