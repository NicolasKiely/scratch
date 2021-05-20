import click


@click.group()
def main():
    pass


@main.group()
def string():
    pass


def do_register_math(main_func):
    @main_func.group()
    def math():
        pass

    @math.command()
    @click.argument("x", type=float)
    @click.argument("y", type=float)
    def add(x, y):
        import controller
        results = controller.do_add(x, y)
        print("%s + %s = %s" % (x, y, results))

    @math.command()
    @click.argument("x", type=int)
    @click.argument("y", type=int)
    def sub(x, y):
        import controller
        results = controller.do_sub(x, y)
        print("%s - %s = %s" % (x, y, results))


do_register_math(main)


@string.command()
@click.argument("string_param", type=str)
def reverse(string_param):
    import controller
    results = controller.do_reverse(string_param)
    print(results)


if __name__ == "__main__":
    main()
