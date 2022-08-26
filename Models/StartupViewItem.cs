using System;

public class StartupViewItem : IComparable
{
    public int IdCount;
    public int Id;
    public string Name;

    public int CompareTo(object obj)
    {
        return (obj as StartupViewItem).IdCount.CompareTo(IdCount);
    }
}