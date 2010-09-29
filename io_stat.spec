require 'citrus'

Citrus.load(File.expand_path('../io_stat', __FILE__))

describe Number do
  context "Integer" do
    subject{ Number.parse('11') }
    it{ should be_a Citrus::Match }
    its(:value){ should == 11 }
  end
  
  context "Float with whitespace" do
    subject{ Number.parse('10.01 ') }
    it{ should be_a Citrus::Match }
    its(:value){ should == 10.01 }
  end
end

describe Word do
  context "Word" do
    subject{ Word.parse('sda2') }
    it{ should be_a Citrus::Match }
    its(:value){ should eql 'sda2' }
  end
  
  context "Word with trailing whitespace" do
    subject{ Word.parse('dm-1 ')}
    it{ should be_a Citrus::Match }
    its(:value){ should eql 'dm-1' }
  end
  
  context "Word starts with %" do
    subject{ Word.parse('%util') }
    it{ should be_a Citrus::Match }
    its(:value){ should eql '%util' }
  end
end

describe List do
  context "Metrics" do
    before do
      @list  = '0.02    84.79  0.24 62.12     5.56  1175.24    18.94     0.07    1.05   0.94   5.85'
      @array = [0.02,84.79,0.24,62.12,5.56,1175.24,18.94,0.07,1.05,0.94,5.85]
    end
    
    subject{ List.parse(@list) }
    it{ should be_a Citrus::Match }
    its(:value){ should eql @array }
  end
  
  context "Device Headings" do
    before do
      @heading  = 'rrqm/s   wrqm/s   r/s   w/s   rsec/s   wsec/s avgrq-sz avgqu-sz   await  svctm  %util'
      @array    = %w(rrqm/s wrqm/s r/s w/s rsec/s wsec/s avgrq-sz avgqu-sz await svctm %util)
    end
    
    subject{ List.parse(@heading) }
    it{ should be_a Citrus::Match }
    its(:value){ should eql @array }
  end
  
  context "CPU Headings" do
    before do
      @heading  = '%user   %nice %system %iowait  %steal   %idle'
      @array    = %w(%user %nice %system %iowait %steal %idle)
    end
    
    subject{ List.parse(@heading) }
    it{ should be_a Citrus::Match }
    its(:value){ should eql @array }
  end
end

describe TimeGrammar do
  context "Timestamp" do
    subject{ TimeGrammar.parse('07:55:34 AM') }
    it{ should be_a Citrus::Match }
    its(:value){ should eql Time.parse('07:55:34 AM') }
  end
end

describe IoStat do
  context "Device Metrics" do
    before do
      @str = 'sda               0.02    84.79  0.24 62.12     5.56  1175.24    18.94     0.07    1.05   0.94'
      @metrics = [0.02, 84.79, 0.24, 62.12, 5.56, 1175.24, 18.94, 0.07, 1.05, 0.94]
    end
    
    subject{ IoStat.parse(@str) }
    it{ should be_a Citrus::Match }
    its(:device){ should eql "sda" }
    its(:metrics){ should eql @metrics }
  end
  
  context "CPU Datapoint" do
    before do
      @str = <<-EOS
avg-cpu:  %user   %nice %system %iowait  %steal   %idle
          38.43    0.00    0.49    0.61    0.00   60.47      
      EOS
      @headings = %w(%user %nice %system %iowait %steal %idle)
      @metrics  = [38.43, 0.00, 0.49, 0.61, 0.00, 60.47]
    end
    
    subject{ IoStat.parse(@str) }
    it{ should be_a Citrus::Match }
    its(:headings_value){ should eql @headings }
    its(:metrics_value){ should eql @metrics }
  end
  
  context "Device Datapoint" do
    before do
      @str = <<-EOS
Device:         rrqm/s   wrqm/s   r/s   w/s   rsec/s   wsec/s avgrq-sz avgqu-sz   await  svctm  %util
sda               0.00     9.58  1.20  1.00    12.77    84.63    44.36     0.01    4.18   3.00   0.66
sda1              0.00     0.00  0.00  0.00     0.00     0.00     0.00     0.00    0.00   0.00   0.00
sda2              0.00     9.58  1.20  1.00    12.77    84.63    44.36     0.01    4.18   3.00   0.66
dm-0              0.00     0.00  1.00 10.58     9.58    84.63     8.14     0.02    2.10   0.57   0.66
dm-1              0.00     0.00  0.00  0.00     0.00     0.00     0.00     0.00    0.00   0.00   0.00      
      EOS
      @headings = %w(rrqm/s wrqm/s r/s w/s rsec/s wsec/s avgrq-sz avgqu-sz await svctm %util)
      @devices  = %w(sda sda1 sda2 dm-0 dm-1)
      @metrics  = [
        [0.00, 9.58, 1.20, 1.00,  12.77, 84.63, 44.36, 0.01, 4.18, 3.00, 0.66],
        [0.00, 0.00, 0.00, 0.00,  0.00,  0.00,  0.00,  0.00, 0.00, 0.00, 0.00],
        [0.00, 9.58, 1.20, 1.00,  12.77, 84.63, 44.36, 0.01, 4.18, 3.00, 0.66],
        [0.00, 0.00, 1.00, 10.58, 9.58,  84.63, 8.14,  0.02, 2.10, 0.57, 0.66],
        [0.00, 0.00, 0.00, 0.00,  0.00,  0.00,  0.00,  0.00, 0.00, 0.00, 0.00]
      ]
    end
    subject{ IoStat.parse(@str) }
    it{ should be_a Citrus::Match }
    its(:headings_value){ should eql @headings }
    its(:devices_value){ should eql @devices }
    its(:metrics_value){ should eql @metrics }
  end
  
  context "IoStat Datapoint" do
    before do
      @str = <<-EOS
Time: 07:55:39 AM
avg-cpu:  %user   %nice %system %iowait  %steal   %idle
          38.43    0.00    0.49    0.61    0.00   60.47

Device:         rrqm/s   wrqm/s   r/s   w/s   rsec/s   wsec/s avgrq-sz avgqu-sz   await  svctm  %util
sda               0.00     9.58  1.20  1.00    12.77    84.63    44.36     0.01    4.18   3.00   0.66
sda1              0.00     0.00  0.00  0.00     0.00     0.00     0.00     0.00    0.00   0.00   0.00
sda2              0.00     9.58  1.20  1.00    12.77    84.63    44.36     0.01    4.18   3.00   0.66
dm-0              0.00     0.00  1.00 10.58     9.58    84.63     8.14     0.02    2.10   0.57   0.66
dm-1              0.00     0.00  0.00  0.00     0.00     0.00     0.00     0.00    0.00   0.00   0.00
      EOS
      @cpu_headings    = %w(%user %nice %system %iowait %steal %idle)
      @cpu_metrics     = [38.43, 0.00, 0.49, 0.61, 0.00, 60.47]
      @device_headings = %w(rrqm/s wrqm/s r/s w/s rsec/s wsec/s avgrq-sz avgqu-sz await svctm %util)
      @device_labels   = %w(sda sda1 sda2 dm-0 dm-1)
      @device_metrics  = [
        [0.00, 9.58, 1.20, 1.00,  12.77, 84.63, 44.36, 0.01, 4.18, 3.00, 0.66],
        [0.00, 0.00, 0.00, 0.00,  0.00,  0.00,  0.00,  0.00, 0.00, 0.00, 0.00],
        [0.00, 9.58, 1.20, 1.00,  12.77, 84.63, 44.36, 0.01, 4.18, 3.00, 0.66],
        [0.00, 0.00, 1.00, 10.58, 9.58,  84.63, 8.14,  0.02, 2.10, 0.57, 0.66],
        [0.00, 0.00, 0.00, 0.00,  0.00,  0.00,  0.00,  0.00, 0.00, 0.00, 0.00]
      ]
      
    end
    
    subject{ IoStat.parse(@str) }
    it{ should be_a Citrus::Match }
    its(:cpu_headings){ should eql @cpu_headings }
    its(:cpu_metrics){ should eql @cpu_metrics }
    its(:device_headings){ should eql @device_headings }
    its(:device_labels){ should eql @device_labels }
    its(:device_metrics){ should eql @device_metrics }
  end
  
  context "IoStat Output File" do
    before do
      @data = File.read( File.expand_path('../cision-iostat-sample.txt', __FILE__) )
    end
    
    subject{ IoStat.parse(@data) }
    it{ should be_a Citrus::Match }
  end
end