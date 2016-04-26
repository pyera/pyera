using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.VisualBasic;
using System.Windows.Forms;
using System.IO;

namespace CSharpTest
{
    class LocaleDump
    {
        static void Main(string[] args)
        {
            var LOCALE = 0x0411; //JAPANESE
            //var LOCALE = 0x0412; //KOREAN
            //var LOCALE = 0x0804; //CHINESE_HANS
            //var LOCALE = 0x0404; //CHINESE_HANT

            using (StreamWriter sw = File.CreateText("map_dumped.txt"))
            {
                for(int i = 0; i < 0x110000; ++i)
                {
                    if (i >= 0xD800 && i < 0xE000)
                        continue;
                    string o = char.ConvertFromUtf32(i);

                    var l = new[] {
                        Strings.StrConv(o, VbStrConv.Narrow, LOCALE),
                        Strings.StrConv(o, VbStrConv.Wide, LOCALE)
                    };
                    if(l.All(x => x == o))
                        continue;
                    sw.Write(i);
                    foreach (var k in l) {
                        sw.Write('\t');
                        sw.Write(char.ConvertToUtf32(k,0));
                    }
                    sw.Write("\r\n");
                }
            }
        }
    }
}
