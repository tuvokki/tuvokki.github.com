desc 'create a new post'
task :post do
  title = ENV['TITLE']
  t = Time.now
  stamp = "#{t.strftime('%Y')}-#{t.strftime('%m')}-#{t.strftime('%d')}"
  slug = "#{stamp}-#{title.gsub(/[^\w]+/, '-')}"

  file = File.join(
    File.dirname(__FILE__),
    '_posts',
    slug + '.md'
  )

  File.open(file, "w") do |f|
    f << <<-EOS.gsub(/^    /, '')
    ---
    layout: post
    title: #{title}
    published: true
    categories:
    ---

    EOS
  end

  # system ("#{ENV['EDITOR']} #{file}")
end

task :default => 'post'